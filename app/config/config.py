import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_URI:str = os.getenv("MONGO_URI")
    DATABASE_NAME:str = os.getenv("DATABASE_NAME")
    JWT_SECRET_KEY:str=os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM:str=os.getenv("JWT_ALGORITHM")
    JWT_EXPIRE_TIME:int=os.getenv("JWT_EXPIRE_TIME")

settings = Settings()