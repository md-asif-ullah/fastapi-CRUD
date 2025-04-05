from fastapi import APIRouter
from models.user_model import UserLogin
from db.mongo import db
from helper.users_helper import serizlized_users_data
from passlib.context import CryptContext
from helper.response_handle import success_response, error_response
from utils.utils import jwt_encoded_data

authRoute = APIRouter(prefix="/api/v1/users",tags=["users"])
collection= db["users"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@authRoute.post("/login", status_code=200)
async def login_user(data:UserLogin):
    try:
        user = await collection.find_one({"email": data.email})
        if not user:
            return error_response(
                message="User not found",
                status_code=404,
            )
        
        if not pwd_context.verify(data.password, user["password"]):
            return error_response(
                message="Invalid password",                                 
                status_code=401,
            )
        # remove password from user data
        user_data = serizlized_users_data(user)
        user_data.pop("password", None) 

        # create token and add it to user data
        user_data["token"]=jwt_encoded_data(user_data)

        return success_response(
            status_code=200,
            message="User logged in successfully",
            data=user_data ,
        )
    
    except Exception as e:
        error_response(
            message=f"An error occurred: {str(e)}",
            status_code=500,
        )
 