from fastapi import FastAPI

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from bcms.database import db

from bcms.routes.auth import router as auth_router
from bcms.routes.user import router as user_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    try:
        yield
    finally:
        await db.disconnect()


app = FastAPI(
    lifespan=lifespan,
    title="Better Club Management System",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.get("/")
async def root():
    return {"message": "I am alive"}


# include all routes
[app.include_router(router) for router in [auth_router, user_router]]
