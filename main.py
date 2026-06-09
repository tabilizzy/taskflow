from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers.auth import auth_router
from routers.projects import pro_router
from routers.comments import task_router
from routers.tasks import proj_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="TaskFlow")


# Unprotected route — anyone can access
@app.get("/")
def health_check():
    return {
        "status": "ok"
        "message: Welcome to the taskflow project"}

app.include_router(auth_router)
app.include_router(pro_router)
app.include_router(proj_router)
app.include_router(task_router)



