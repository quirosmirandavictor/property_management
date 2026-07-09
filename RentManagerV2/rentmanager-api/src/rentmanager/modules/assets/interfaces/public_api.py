from fastapi import APIRouter

from rentmanager.modules.assets.interfaces.api.router import router as assets_router


def get_router() -> APIRouter:
	api_router = APIRouter(prefix="/api/v1")
	api_router.include_router(assets_router)
	return api_router
