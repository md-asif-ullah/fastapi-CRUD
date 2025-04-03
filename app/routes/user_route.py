from fastapi import APIRouter, HTTPException
from models.user_model import User
from db.mongo import db
from helper.users_helper import serizlized_users_data


userRoute = APIRouter(prefix="/api/v1/users",tags=["users"])
collection= db["users"]



@userRoute.post("/")
async def create_user(user: User):
    try:
        user_dict = user.model_dump()
        result = await collection.insert_one(user_dict)

        return {"message": "User added successfully", "data": {"id": str(result.inserted_id)}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@userRoute.get("/")
async def get_user():
    all_users = await collection.find().to_list(length=None)
    serizlized_users=[serizlized_users_data(user) for user in all_users]


    return {"message": "Users return successfully", "data": serizlized_users}

