from fastapi.testclient import TestClient

from rentmanager.main import app
from rentmanager.modules.iam.application.use_cases.authenticate_user import AuthenticatedUser
from rentmanager.modules.iam.interfaces.api.dependencies import get_authenticate_user_use_case
from rentmanager.modules.iam.interfaces.api.dependencies import get_jwt_provider
from rentmanager.modules.iam.interfaces.api.dependencies import get_refresh_token_repository
from rentmanager.shared_kernel.infrastructure.security.jwt_provider import JwtProvider


class _FakeAuthenticateUserUseCase:
    def execute(self, username: str, password: str) -> AuthenticatedUser:
        if username != "admin" or password != "admin123":
            raise ValueError("invalid credentials")
        return AuthenticatedUser(user_id=1, username=username)


class _FakeRefreshTokenRecord:
    def __init__(self, user_id: int, jti: str, expires_at, revoked_at=None) -> None:
        self.user_id = user_id
        self.jti = jti
        self.expires_at = expires_at
        self.revoked_at = revoked_at


class _FakeRefreshTokenRepository:
    def __init__(self) -> None:
        self._items: dict[str, _FakeRefreshTokenRecord] = {}

    def add(self, token):
        record = _FakeRefreshTokenRecord(
            user_id=token.user_id,
            jti=token.jti,
            expires_at=token.expires_at,
            revoked_at=token.revoked_at,
        )
        self._items[token.jti] = record
        return token

    def get_by_jti(self, jti: str):
        return self._items.get(jti)

    def revoke(self, jti: str) -> None:
        record = self._items.get(jti)
        if record is not None:
            record.revoked_at = record.expires_at


_refresh_repo = _FakeRefreshTokenRepository()
_jwt_provider = JwtProvider(
    algorithm="RS256",
    private_key_pem=None,
    public_key_pem=None,
    allow_ephemeral_keys=True,
)


def _override_auth_use_case() -> _FakeAuthenticateUserUseCase:
    return _FakeAuthenticateUserUseCase()


def _override_refresh_repo() -> _FakeRefreshTokenRepository:
    return _refresh_repo


def _override_jwt_provider() -> JwtProvider:
    return _jwt_provider


def test_login_and_me() -> None:
    app.dependency_overrides[get_authenticate_user_use_case] = _override_auth_use_case
    app.dependency_overrides[get_refresh_token_repository] = _override_refresh_repo
    app.dependency_overrides[get_jwt_provider] = _override_jwt_provider

    client = TestClient(app)

    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert isinstance(login_response.json()["refresh_token"], str)

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    assert me_response.json() == {"user_id": 1, "username": "admin"}

    app.dependency_overrides.clear()
