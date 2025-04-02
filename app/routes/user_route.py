from fastapi import APIRouter, HTTPException
from models.user_model import User
from db.mongo import db

userRoute = APIRouter()
collection= db["users"]


@userRoute.post("/users/")
async def create_user(user: User):
    try:
        user_dict = user.model_dump()
        result = await collection.insert_one(user_dict)

        return {"message": "User added successfully", "data": {"id": str(result.inserted_id)}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")