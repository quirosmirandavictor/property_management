from dataclasses import dataclass

from rentmanager.shared_kernel.infrastructure.security.password_hasher import PasswordHasher


@dataclass(frozen=True)
class AuthenticatedUser:
	username: str


class AuthenticateUserUseCase:
	"""Auth skeleton for phase 0 using in-memory users."""

	def __init__(self, password_hasher: PasswordHasher) -> None:
		self._password_hasher = password_hasher
		self._users = {
			"admin": self._password_hasher.hash("admin123"),
		}

	def execute(self, username: str, password: str) -> AuthenticatedUser | None:
		password_hash = self._users.get(username)
		if password_hash is None:
			return None

		if not self._password_hasher.verify(password, password_hash):
			return None

		return AuthenticatedUser(username=username)

