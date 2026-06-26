from fastapi import APIRouter

from rentmanager.modules.iam.interfaces.api.router import router as auth_router


def get_router() -> APIRouter:
	api_router = APIRouter(prefix="/api/v1")
	api_router.include_router(auth_router)
	return api_router

