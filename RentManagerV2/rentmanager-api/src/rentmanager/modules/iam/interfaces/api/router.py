from fastapi import APIRouter, Depends, HTTPException, status

from rentmanager.config import Settings, get_settings
from rentmanager.modules.iam.application.use_cases.authenticate_user import (
	AuthenticateUserUseCase,
)
from rentmanager.modules.iam.interfaces.api.dependencies import (
	get_authenticate_user_use_case,
	get_current_username,
	get_jwt_provider,
)
from rentmanager.modules.iam.interfaces.api.schemas import (
	CurrentUserResponse,
	LoginRequest,
	LoginResponse,
)
from rentmanager.shared_kernel.infrastructure.security.jwt_provider import JwtProvider

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
	payload: LoginRequest,
	use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
	jwt_provider: JwtProvider = Depends(get_jwt_provider),
	settings: Settings = Depends(get_settings),
) -> LoginResponse:
	user = use_case.execute(username=payload.username, password=payload.password)
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid credentials",
		)

	token = jwt_provider.create_access_token(
		subject=user.username,
		expires_minutes=settings.access_token_expire_minutes,
	)
	return LoginResponse(access_token=token)


@router.get("/me", response_model=CurrentUserResponse)
def me(username: str = Depends(get_current_username)) -> CurrentUserResponse:
	return CurrentUserResponse(username=username)

