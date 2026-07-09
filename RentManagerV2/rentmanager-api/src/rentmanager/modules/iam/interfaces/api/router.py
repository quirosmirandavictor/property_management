from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from rentmanager.config import Settings, get_settings
from rentmanager.modules.iam.application.use_cases.authenticate_user import (
	AuthenticateUserUseCase,
)
from rentmanager.modules.iam.domain.entities import RefreshToken
from rentmanager.modules.iam.domain.exceptions import InvalidCredentialsError
from rentmanager.modules.iam.domain.exceptions import UserInactiveError
from rentmanager.modules.iam.interfaces.api.dependencies import (
	get_authenticate_user_use_case,
	get_current_user_id,
	get_current_username,
	get_jwt_provider,
	get_refresh_token_repository,
)
from rentmanager.modules.iam.domain.repositories import RefreshTokenRepository
from rentmanager.modules.iam.interfaces.api.schemas import (
	CurrentUserResponse,
	LoginRequest,
	LoginResponse,
	LogoutRequest,
	RefreshTokenRequest,
)
from rentmanager.shared_kernel.infrastructure.security.jwt_provider import JwtProvider

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
	"/login",
	response_model=LoginResponse,
	summary="Authenticate user",
	description="Validate credentials and issue one access token plus one refresh token.",
	responses={
		401: {"description": "Invalid credentials or inactive user."},
		500: {"description": "Refresh token payload generation failed."},
	},
)
def login(
	payload: LoginRequest,
	use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
	jwt_provider: JwtProvider = Depends(get_jwt_provider),
	refresh_tokens: RefreshTokenRepository = Depends(get_refresh_token_repository),
	settings: Settings = Depends(get_settings),
) -> LoginResponse:
	try:
		user = use_case.execute(username=payload.username, password=payload.password)
	except (InvalidCredentialsError, UserInactiveError) as exc:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=str(exc),
		) from exc

	access_token = jwt_provider.create_access_token(
		subject=user.username,
		user_id=user.user_id,
		expires_minutes=settings.access_token_expire_minutes,
	)
	refresh_token = jwt_provider.create_refresh_token(
		subject=user.username,
		expires_days=settings.refresh_token_expire_days,
	)

	payload_refresh = jwt_provider.decode_token(refresh_token)
	jti = payload_refresh.get("jti")
	expires_at_unix = payload_refresh.get("exp")
	if not isinstance(jti, str) or not isinstance(expires_at_unix, int):
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Invalid refresh token payload generated.",
		)

	refresh_tokens.add(
		RefreshToken(
			id=None,
			user_id=user.user_id,
			jti=jti,
			expires_at=datetime.fromtimestamp(expires_at_unix, tz=UTC),
		)
	)

	return LoginResponse(
		access_token=access_token,
		refresh_token=refresh_token,
		expires_in=settings.access_token_expire_minutes * 60,
	)


@router.post(
	"/refresh",
	response_model=LoginResponse,
	summary="Rotate refresh token",
	description="Revoke current refresh token and return a new access/refresh token pair.",
	responses={
		401: {"description": "Refresh token invalid, revoked, unknown, or expired."},
		500: {"description": "Refresh token payload generation failed."},
	},
)
def refresh_token(
	payload: RefreshTokenRequest,
	jwt_provider: JwtProvider = Depends(get_jwt_provider),
	refresh_tokens: RefreshTokenRepository = Depends(get_refresh_token_repository),
	settings: Settings = Depends(get_settings),
) -> LoginResponse:
	try:
		token_payload = jwt_provider.decode_token(payload.refresh_token)
	except Exception as exc:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token",
		) from exc

	if token_payload.get("typ") != "refresh":
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token type",
		)

	subject = token_payload.get("sub")
	jti = token_payload.get("jti")
	expires_at_unix = token_payload.get("exp")
	if not isinstance(subject, str) or not isinstance(jti, str) or not isinstance(expires_at_unix, int):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token payload",
		)

	persisted = refresh_tokens.get_by_jti(jti)
	if persisted is None or persisted.revoked_at is not None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Refresh token revoked or unknown",
		)
	persisted_expires_at = persisted.expires_at
	if persisted_expires_at.tzinfo is None:
		persisted_expires_at = persisted_expires_at.replace(tzinfo=UTC)
	if persisted_expires_at < datetime.now(UTC):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Refresh token expired",
		)

	refresh_tokens.revoke(jti)

	access_token = jwt_provider.create_access_token(
		subject=subject,
		user_id=persisted.user_id,
		expires_minutes=settings.access_token_expire_minutes,
	)
	new_refresh_token = jwt_provider.create_refresh_token(
		subject=subject,
		expires_days=settings.refresh_token_expire_days,
	)

	new_payload = jwt_provider.decode_token(new_refresh_token)
	new_jti = new_payload.get("jti")
	new_exp = new_payload.get("exp")
	if not isinstance(new_jti, str) or not isinstance(new_exp, int):
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Invalid refresh token payload generated.",
		)

	refresh_tokens.add(
		RefreshToken(
			id=None,
			user_id=persisted.user_id,
			jti=new_jti,
			expires_at=datetime.fromtimestamp(new_exp, tz=UTC),
		)
	)

	return LoginResponse(
		access_token=access_token,
		refresh_token=new_refresh_token,
		expires_in=settings.access_token_expire_minutes * 60,
	)


@router.post(
	"/logout",
	status_code=status.HTTP_204_NO_CONTENT,
	summary="Logout user",
	description="Invalidate one refresh token to terminate session continuity.",
	responses={
		204: {"description": "Refresh token revoked successfully."},
		401: {"description": "Refresh token is invalid or malformed."},
	},
)
def logout(
	payload: LogoutRequest,
	jwt_provider: JwtProvider = Depends(get_jwt_provider),
	refresh_tokens: RefreshTokenRepository = Depends(get_refresh_token_repository),
) -> None:
	try:
		token_payload = jwt_provider.decode_token(payload.refresh_token)
	except Exception as exc:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token",
		) from exc

	if token_payload.get("typ") != "refresh":
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token type",
		)

	jti = token_payload.get("jti")
	if not isinstance(jti, str):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token payload",
		)

	refresh_tokens.revoke(jti)


@router.get(
	"/me",
	response_model=CurrentUserResponse,
	summary="Get authenticated user",
	description="Return identity information extracted from the current access token.",
	responses={
		401: {"description": "Missing or invalid access token."},
	},
)
def me(
	user_id: int = Depends(get_current_user_id),
	username: str = Depends(get_current_username),
) -> CurrentUserResponse:
	return CurrentUserResponse(user_id=user_id, username=username)

