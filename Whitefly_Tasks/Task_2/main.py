from fastapi import FastAPI, HTTPException
from models import User
from typing import List

app = FastAPI()

users_db = []

@app.post("/users/", response_model=User)
def create_user(user: User):
    for existing_user in users_db:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="This email is already registered.")

    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    return users_db