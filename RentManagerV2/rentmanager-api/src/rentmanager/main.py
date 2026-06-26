from fastapi import FastAPI

from rentmanager.config import get_settings
from rentmanager.modules.iam.interfaces.public_api import get_router as get_iam_router

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.app_debug)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
	return {"status": "ok"}


app.include_router(get_iam_router())

