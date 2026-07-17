from fastapi import FastAPI

from rentmanager.config import Settings, get_settings
from rentmanager.modules.assets.interfaces.public_api import get_router as get_assets_router
from rentmanager.modules.contracts.interfaces.public_api import get_router as get_contracts_router
from rentmanager.modules.iam.interfaces.public_api import get_router as get_iam_router


def create_app(settings: Settings | None = None) -> FastAPI:
	resolved_settings = settings or get_settings()
	docs_enabled = not resolved_settings.production_env

	app = FastAPI(
		title=resolved_settings.app_name,
		description=(
			"RentManager modular monolith API. Authentication and authorization are centralized "
			"in IAM and reused by business modules."
		),
		debug=resolved_settings.app_debug,
		version="0.1.0",
		docs_url="/docs" if docs_enabled else None,
		redoc_url="/redoc" if docs_enabled else None,
		openapi_url="/openapi.json" if docs_enabled else None,
	)

	@app.get(
		"/health",
		tags=["health"],
		summary="Health check",
		description="Liveness endpoint used by orchestrators and uptime monitors.",
	)
	def health() -> dict[str, str]:
		return {"status": "ok"}

	app.include_router(get_iam_router())
	app.include_router(get_assets_router())
	app.include_router(get_contracts_router())
	return app

app = create_app()

