from fastapi import APIRouter
from models.user_model import User,updateName
from db.mongo import db
from helper.users_helper import serizlized_users_data
from passlib.context import CryptContext
from helper.response_handle import success_response, error_response


userRoute = APIRouter(prefix="/api/v1/users",tags=["users"])
collection= db["users"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@userRoute.post("/", status_code=201)
async def create_user(user: User):
    try:
        user_dict = user.model_dump()

        # check if user already exists
        user_exist = await collection.find_one({"email": user_dict["email"]})
        if user_exist:  
            return error_response(
                message="User already exists",
                status_code=400,
            )

        # encrypt password
        user_dict["password"] = pwd_context.hash(user_dict["password"])

        result = await collection.insert_one(user_dict)

        return success_response(
            status_code=201,
            message="User added successfully",
            data={"id": [str(result.inserted_id)]},
        )
    
    except Exception as e:
        raise error_response(
            message=f"An error occurred: {str(e)}",
            status_code=500,
        )
    

@userRoute.get("/")
async def get_user():
    try:
        all_users = await collection.find().to_list(length=None)
        serizlized_users = []
        for user in all_users:
            user_data = serizlized_users_data(user)
            user_data.pop("password", None) 
            serizlized_users.append(user_data)
    
        return success_response(
            status_code=200,
            message="Users return successfully",
            data=serizlized_users,
        )
    except Exception as e:
     raise error_response(
            message=f"An error occurred: {str(e)}",
            status_code=500,
        )
   


@userRoute.get("/{user_email}", status_code=200)
async def get_user_by_id(user_email: str):
    try:

        user = await collection.find_one({"email": user_email})
        if not user:
            return error_response(
                message="User not found",
                status_code=404,
            )
        
        user_data = serizlized_users_data(user)
        user_data.pop("password", None) 
        return success_response(
            status_code=200,
            message="User returned successfully",
            data=user_data,
        )
    
    except Exception as e:
        raise error_response(
            message=f"An error occurred: {str(e)}",
            status_code=500,
        )
    

@userRoute.put("/{user_email}", status_code=200)
async def update_name(user_email:str,payload:updateName):
    try:

    
        user = await collection.find_one({"email": user_email})
        if not user:
            return error_response(
                message="User not found",
                status_code=404,
            )
        
        update_user= await collection.update_one(
            {"email": user_email},
            {"$set": {"name":payload.name}},
        )

        if update_user.modified_count == 0:
            return error_response(
                message="User not updated",
                status_code=400,
            )
        print(update_user)
        return success_response(
            status_code=200,
            message="User updated successfully",
            data=[],
        )
    
    except Exception as e:
        raise error_response(
            message=f"An error occurred: {str(e)}",
            status_code=500,
        )