FROM python:3.12.6

# Set the working directory
WORKDIR /code

# Copy the requirements file to the working directory
COPY ./requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY ./app ./app

# Command to run FastAPI app
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
