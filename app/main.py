from fastapi import FastAPI
from routes.user_route import userRoute

app = FastAPI()

@app.get("/")
def root():
    return {"message":"server running"}

app.include_router(userRoute)
