from fastapi import HTTPException
import httpx


def check_valid_breed(breed_name):
    breeds = httpx.get("https://dog.ceo/api/breeds/list/all")
    breeds = breeds.json()
    if breed_name not in breeds["message"]:
        raise HTTPException(status_code=400, detail="Invalid breed")

def get_image_url(breed_name):
    response = httpx.get(f"https://dog.ceo/api/breed/{breed_name}/images/random")
    data = response.json()
    image_url = data["message"]

    if data["status"] == "error":
        raise HTTPException(status_code=500, detail="Failed to fetch dog image")
    return image_url