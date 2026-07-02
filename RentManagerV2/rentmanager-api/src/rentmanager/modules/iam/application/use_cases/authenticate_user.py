from dataclasses import dataclass

from rentmanager.modules.iam.domain.repositories import UserRepository
from rentmanager.modules.iam.domain.exceptions import InvalidCredentialsError
from rentmanager.modules.iam.domain.exceptions import UserInactiveError
from rentmanager.shared_kernel.infrastructure.security.password_hasher import PasswordHasher


@dataclass(frozen=True)
class AuthenticatedUser:
	user_id: int
	username: str


class AuthenticateUserUseCase:
	"""Authenticate users against IAM repository using secure password verification."""

	def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher) -> None:
		self._user_repository = user_repository
		self._password_hasher = password_hasher

	def execute(self, username: str, password: str) -> AuthenticatedUser:
		user = self._user_repository.get_by_username(username)
		if user is None:
			raise InvalidCredentialsError("Invalid username or password.")

		if not user.is_active:
			raise UserInactiveError("Inactive users cannot authenticate.")

		if not self._password_hasher.verify(password, user.password_hash):
			raise InvalidCredentialsError("Invalid username or password.")

		if user.id is None:
			raise InvalidCredentialsError("User identity is invalid.")

		return AuthenticatedUser(user_id=user.id, username=user.username)

