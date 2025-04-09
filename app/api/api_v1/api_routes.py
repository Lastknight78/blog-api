from fastapi import APIRouter
from .endpoints import account, auth
from .endpoints.admin import router


api_router = APIRouter()


api_router.include_router(account.router, prefix="/accounts", tags=["account"])
api_router.include_router(auth.router, tags=["auth"])

# admin
api_router.include_router(router, prefix="/admin")
