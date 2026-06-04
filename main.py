from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers.auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="TaskFlow")


app.include_router(auth_router)
