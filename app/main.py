import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException
from app import database
from app.utils import check_valid_breed, get_image_url
from app import auth
from passlib.context import CryptContext


app = FastAPI(description="Dog Wrapper API", version="1.0")

# Connect to MongoDB
db = database.MongoDB()
users_db = database.MongoDBUsers()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(
        users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    # Create access token with a 30-minute expiration
    access_token = auth.create_access_token(data={"sub": user["username"]})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users")
async def create_user(user: auth.User):
    # Check if the user already exists
    if users_db.get_user(user.username):
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_password = pwd_context.encrypt(user.password)

    # Convert the user model to a dictionary
    user_dict = user.model_dump()  # Convert Pydantic model to dictionary

    # Add the hashed password to the dictionary
    user_dict["password"] = hashed_password

    # Insert the user into the database
    users_db.insert_one(user_dict)

    return {"message": "User created successfully"}


@app.get("/dog/breed/{breed_name}")
async def images_breed(breed_name: str, token: str = Depends(oauth2_scheme)):

    # Check if the breed is in the database
    check_valid_breed(breed_name)
    # Get the image from the API
    image_url = get_image_url(breed_name)

    document = {
        "breed": breed_name,
        "url": image_url,
        "timestamp": str(datetime.datetime.now()),
        "status": "success"
    }
    db.insert_one(document)
    return {"image": image_url, "message": "success"}


@app.get("/dog/stats")
async def stats(token: str = Depends(oauth2_scheme)):
    # Get the top 10 breeds
    breeds = db.get_top_breeds()
    # Stats is built as follows:
    # Stats is a list of dictionaries, where each dictionary contains the breed and the number of requests for that breed.
    # Stats:[{breed: "labrador", requests: 10}, {breed: "bulldog", requests: 5}]
    stats = [{"breed": breed["_id"], "requests": breed["count"]}
             for breed in breeds]
    return {"stats": stats}
