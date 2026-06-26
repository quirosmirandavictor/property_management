from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
	username: str = Field(min_length=3, max_length=100)
	password: str = Field(min_length=6, max_length=200)


class LoginResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
	username: str

