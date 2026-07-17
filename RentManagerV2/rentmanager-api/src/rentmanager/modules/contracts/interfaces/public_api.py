from fastapi import APIRouter

from rentmanager.modules.contracts.interfaces.api.router import router as contracts_router


def get_router() -> APIRouter:
	api_router = APIRouter(prefix="/api/v1")
	api_router.include_router(contracts_router)
	return api_router
