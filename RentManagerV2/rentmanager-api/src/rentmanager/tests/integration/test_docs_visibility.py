from rentmanager.config import Settings
from rentmanager.main import create_app


def test_docs_enabled_when_not_production() -> None:
    app = create_app(Settings(production_env=False))

    assert app.docs_url == "/docs"
    assert app.redoc_url == "/redoc"
    assert app.openapi_url == "/openapi.json"


def test_docs_disabled_when_production_env() -> None:
    app = create_app(Settings(production_env=True))

    assert app.docs_url is None
    assert app.redoc_url is None
    assert app.openapi_url is None
