# Dog Wrapper API

## Description

The Dog Wrapper API is a FastAPI-based application that provides endpoints to interact with dog breed data, including fetching breed images, managing user authentication, and providing breed statistics. This API connects to a MongoDB database to store user information and breed-related data.

## Features

- **User Authentication**: Users can log in using OAuth2 to receive an access token.
- **User Creation**: Allows the creation of new users with password hashing.
- **Breed Image Retrieval**: Fetches images for a given dog breed.
- **Breed Stats**: Provides statistics on the most requested dog breeds.

## API Endpoints

### 1. **`POST /token`**
   - **Description**: Logs in a user and returns an access token.
   - **Body Parameters**:
     - `username` (str): The username of the user.
     - `password` (str): The password of the user.
   - **Response**:
     - `access_token` (str): The bearer token for authentication.
     - `token_type` (str): The type of the token (bearer).

### 2. **`POST /users`**
   - **Description**: Creates a new user.
   - **Body Parameters**:
     - `username` (str): The username for the new user.
     - `password` (str): The password for the new user.
   - **Response**:
     - `message` (str): Confirmation message indicating the user was created.

### 3. **`GET /dog/breed/{breed_name}`**
   - **Description**: Retrieves an image for a given dog breed.
   - **Path Parameters**:
     - `breed_name` (str): The name of the dog breed.
   - **Headers**:
     - `token` (str): The OAuth2 token required for authentication.
   - **Response**:
     - `image` (str): URL of the breed's image.
     - `message` (str): Confirmation message.

### 4. **`GET /dog/stats`**
   - **Description**: Provides statistics on the top 10 most requested dog breeds.
   - **Headers**:
     - `token` (str): The OAuth2 token required for authentication.
   - **Response**:
     - `stats` (list): A list of dictionaries containing breed names and their request counts.

## Installation and Setup

### Prerequisites

- **Python 3.12+**: Ensure Python 3.12.6 or higher is installed on your system.
- **MongoDB**: A running MongoDB instance (local or cloud). If you don't have MongoDB installed, follow the instructions below to set it up locally.

### Steps to Install and Run the API

1. **Clone the Repository**
   - Clone this repository to your local machine:
     ```bash
     git clone <repo-url>
     cd <repo-folder>
     ```

2. **Create a Virtual Environment**
   - It is recommended to create a virtual environment for the project:
     ```bash
     python3 -m venv venv
     ```

3. **Activate the Virtual Environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**
   - Install all the required Python dependencies using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

### Setting Up MongoDB Locally

1. **Install MongoDB**
   - Follow the installation guide for MongoDB:  
     [Install MongoDB](https://www.mongodb.com/docs/manual/installation/)
   - Or use a container with MongoDB (preferred).

2. **Start MongoDB**
   - Once MongoDB is installed, start the MongoDB server:
     ```bash
     mongod
     ```
    - Or start an intance of a mongodb container

### Setting the .env File

Ensure you have the following environment variables set in your `.env` file whith the information for the jwt token and mongo url:
- `SECRET_KEY`
- `MONGO_URI`

### Running Locally

To run the FastAPI application:

```bash
fastapi run app/main.py
```

To run the tests:
```bash
pytest tests/pytest.py