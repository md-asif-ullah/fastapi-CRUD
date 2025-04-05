from fastapi import FastAPI
from routes.user_route import userRoute
from routes.auth_route import authRoute


app = FastAPI()

@app.get("/")
def root():
    return {"message":"server running"}

app.include_router(userRoute)
app.include_router(authRoute)