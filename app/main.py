from fastapi import FastAPI
from app.routes.user import user

app = FastAPI()
app.include_router(user.router)


@app.get("/check")
async def check():
    return {"message": "Hello World"}
