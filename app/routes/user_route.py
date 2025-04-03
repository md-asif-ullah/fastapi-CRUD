from fastapi import APIRouter, HTTPException
from models.user_model import User
from db.mongo import db
from helper.users_helper import serizlized_users_data
from passlib.context import CryptContext


userRoute = APIRouter(prefix="/api/v1/users",tags=["users"])
collection= db["users"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@userRoute.post("/")
async def create_user(user: User):
    try:
        user_dict = user.model_dump()

        # check use exist
        user_exist = await collection.find_one({"email": user_dict["email"]})
        if user_exist:
            return {"message": "user already exist"}

        # encrypt password
        user_dict["password"] = pwd_context.hash(user_dict["password"])

        result = await collection.insert_one(user_dict)

        return {"message": "User added successfully", "data": {"id": [str(result.inserted_id)]}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@userRoute.get("/")
async def get_user():
    all_users = await collection.find().to_list(length=None)
    serizlized_users = []
    for user in all_users:
        user_data = serizlized_users_data(user)
        user_data.pop("password", None) 
        serizlized_users.append(user_data)
   

    return {"message": "Users return successfully", "data": serizlized_users}

