from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import logging

app = FastAPI()

users = {}

class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    height: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Creation App!"}


@app.post("/create_user", status_code=201)  
async def create_user(user: User):
    if user.email in users:
        # If the email already exists, return a 400 error
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    # Store the user data in the dictionary using the email as the unique key
    users[user.email] = user.dict()
    
    return {"message": "User created successfully", "user": user}

# Allow only requests from localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Specify allowed origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods 
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(f"Request to {request.url.path} took {duration:.4f} seconds")
    return response




