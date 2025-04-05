from fastapi import APIRouter
from .endpoints import account
from .endpoints.admin import router


api_router = APIRouter()


api_router.include_router(account.router, prefix="/accounts", tags=["account"])

# admin
api_router.include_router(router, prefix="/admin")
