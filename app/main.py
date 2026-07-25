from fastapi import FastAPI

from app.routers import auth_router, user_router


# ==========================
# Application
# ==========================

app = FastAPI(
    title="Own SQL FastAPI",
    version="1.0.0"
)

# ==========================
# Routers
# ==========================

app.include_router(
    auth_router.router
)

app.include_router(
    user_router.router
)