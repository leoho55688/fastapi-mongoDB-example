from fastapi import APIRouter

from app.api.routes import authentication, interviews, jobs, llm, users
from app.api.routes import test

router = APIRouter()

router.include_router(authentication.router, tags=["auth"], prefix="/auth")
router.include_router(users.router, tags=["users"], prefix="/user")