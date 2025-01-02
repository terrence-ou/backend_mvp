from fastapi import FastAPI
from app.routes.user import user
from app.routes.generate import generate

app = FastAPI()
app.include_router(user.router)
app.include_router(generate.router)


@app.get("/check")
async def check():
    return {"message": "Hello World"}
