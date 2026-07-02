from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from rentmanager.config import Settings, get_settings, resolve_project_path
from rentmanager.modules.iam.application.use_cases.authenticate_user import (
	AuthenticateUserUseCase,
)
from rentmanager.modules.iam.domain.repositories import RefreshTokenRepository
from rentmanager.modules.iam.domain.repositories import UserRepository
from rentmanager.modules.iam.infrastructure.repositories_sqlalchemy import SqlAlchemyRefreshTokenRepository
from rentmanager.modules.iam.infrastructure.repositories_sqlalchemy import SqlAlchemyUserRepository
from rentmanager.shared_kernel.infrastructure.db.session import get_db_session
from rentmanager.shared_kernel.infrastructure.security.jwt_provider import JwtProvider
from rentmanager.shared_kernel.infrastructure.security.password_hasher import PasswordHasher

auth_scheme = HTTPBearer(auto_error=False)


def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepository:
	return SqlAlchemyUserRepository(session=session)


def get_refresh_token_repository(
	session: Session = Depends(get_db_session),
) -> RefreshTokenRepository:
	return SqlAlchemyRefreshTokenRepository(session=session)


def get_authenticate_user_use_case(
	user_repository: UserRepository = Depends(get_user_repository),
) -> AuthenticateUserUseCase:
	return AuthenticateUserUseCase(
		user_repository=user_repository,
		password_hasher=PasswordHasher(),
	)


def get_jwt_provider(settings: Settings = Depends(get_settings)) -> JwtProvider:
	private_pem = _read_pem_file(resolve_project_path(settings.jwt_private_key_path))
	public_pem = _read_pem_file(resolve_project_path(settings.jwt_public_key_path))
	return JwtProvider(
		algorithm=settings.jwt_algorithm,
		private_key_pem=private_pem,
		public_key_pem=public_pem,
		allow_ephemeral_keys=settings.app_env in {"dev", "test"},
	)


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

	if payload.get("typ") != "access":
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token type",
		)

	subject = payload.get("sub")
	if not isinstance(subject, str) or not subject:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token payload",
		)
	return subject


def get_current_user_id(
	credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
	jwt_provider: JwtProvider = Depends(get_jwt_provider),
) -> int:
	"""Return current user identifier from a validated access token."""

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

	if payload.get("typ") != "access":
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token type",
		)

	user_id_value = payload.get("uid")
	if not isinstance(user_id_value, int):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token payload",
		)

	return user_id_value


def require_functionality(functionality_code: str):
	"""Build a reusable authorization dependency for protected endpoints."""

	def dependency(
		username: str = Depends(get_current_username),
		user_repository: UserRepository = Depends(get_user_repository),
	) -> None:
		user = user_repository.get_by_username(username)
		if user is None or not user.is_active:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid authenticated user",
			)

		granted_codes = {
			functionality.code
			for role in user.roles
			for functionality in role.functionalities
		}
		if functionality_code not in granted_codes:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Insufficient permissions",
			)

	return dependency


def _read_pem_file(file_path: Path) -> str | None:
	"""Read one PEM file when available, returning None when missing."""

	if not file_path.exists():
		return None
	return file_path.read_text(encoding="utf-8")

