from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
	username: str = Field(min_length=3, max_length=100)
	password: str = Field(min_length=6, max_length=200)


class LoginResponse(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"
	expires_in: int


class RefreshTokenRequest(BaseModel):
	refresh_token: str = Field(min_length=30)


class LogoutRequest(BaseModel):
	refresh_token: str = Field(min_length=30)


class CurrentUserResponse(BaseModel):
	user_id: int
	username: str

