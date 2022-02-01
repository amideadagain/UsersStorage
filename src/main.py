import uvicorn
from fastapi import FastAPI

from src.db import db
from src.routers import users

app = FastAPI(title="Async FastAPI")

app.include_router(users.router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
