from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

# Create an in-memory storage for user data (just a dictionary for now)
users = {}

# Define a Pydantic model for the user data
class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    height: float

# POST endpoint to create a new user
@app.post("/create_user", status_code=201)
async def create_user(user: User):
    if user.email in users:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    users[user.email] = user.dict()  # Store the user data in memory
    return {"message": "User created successfully", "user": user}

# Optional: A GET endpoint to retrieve a user by email (for testing purposes)
@app.get("/get_user/{email}")
async def get_user(email: str):
    user = users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
