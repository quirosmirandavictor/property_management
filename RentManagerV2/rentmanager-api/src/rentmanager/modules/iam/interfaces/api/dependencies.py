from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from rentmanager.config import Settings, get_settings
from rentmanager.modules.iam.application.use_cases.authenticate_user import (
	AuthenticateUserUseCase,
)
from rentmanager.shared_kernel.infrastructure.security.jwt_provider import JwtProvider
from rentmanager.shared_kernel.infrastructure.security.password_hasher import PasswordHasher

auth_scheme = HTTPBearer(auto_error=False)


def get_authenticate_user_use_case() -> AuthenticateUserUseCase:
	return AuthenticateUserUseCase(password_hasher=PasswordHasher())


def get_jwt_provider(settings: Settings = Depends(get_settings)) -> JwtProvider:
	return JwtProvider(secret_key=settings.app_secret_key)


def get_current_username(
	credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
	jwt_provider: JwtProvider = Depends(get_jwt_provider),
) -> str:
	if credentials is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authenticated",
		)

	try:
		payload = jwt_provider.decode_token(credentials.credentials)
	except Exception as exc:  # pragma: no cover
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token",
		) from exc

	subject = payload.get("sub")
	if not isinstance(subject, str) or not subject:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token payload",
		)
	return subject

