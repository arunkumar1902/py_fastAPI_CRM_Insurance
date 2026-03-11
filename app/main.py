from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import add_new_user, add_new_policy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

@app.get("/")
def server():
    return {"message":"Server Started"}

app.include_router(add_new_user.router)
app.include_router(add_new_policy.router)