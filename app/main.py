from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.redis import redis_client
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.ping()
    yield
    await redis_client.aclose()


app = FastAPI(
    title="Own SQL FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(user_router)