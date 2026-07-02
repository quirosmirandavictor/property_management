from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from rentmanager.modules.iam.domain.entities import Functionality
from rentmanager.modules.iam.domain.entities import RefreshToken
from rentmanager.modules.iam.domain.entities import Role
from rentmanager.modules.iam.domain.entities import User


class UserRepository(ABC):
	"""Contract for persisting and retrieving IAM users."""

	@abstractmethod
	def add(self, user: User) -> User:
		"""Persist a new user aggregate and return its current state."""

	@abstractmethod
	def update(self, user: User) -> User:
		"""Persist scalar changes for an existing user aggregate."""

	@abstractmethod
	def get_by_id(self, user_id: int) -> User | None:
		"""Return one user aggregate by its identifier."""

	@abstractmethod
	def get_by_username(self, username: str) -> User | None:
		"""Return one user aggregate by its login name."""

	@abstractmethod
	def get_by_email(self, email: str) -> User | None:
		"""Return one user aggregate by its email address."""

	@abstractmethod
	def list(self, *, is_active: bool | None = None) -> Sequence[User]:
		"""Return users filtered by optional activation state."""

	@abstractmethod
	def assign_role(self, user_id: int, role_id: int) -> None:
		"""Attach a role to a user if the association does not already exist."""

	@abstractmethod
	def remove_role(self, user_id: int, role_id: int) -> None:
		"""Detach a role from a user if the association exists."""

	@abstractmethod
	def delete(self, user_id: int) -> None:
		"""Delete one user aggregate by identifier."""


class RoleRepository(ABC):
	"""Contract for persisting and retrieving IAM roles."""

	@abstractmethod
	def add(self, role: Role) -> Role:
		"""Persist a new role aggregate and return its current state."""

	@abstractmethod
	def update(self, role: Role) -> Role:
		"""Persist scalar changes for an existing role aggregate."""

	@abstractmethod
	def get_by_id(self, role_id: int) -> Role | None:
		"""Return one role aggregate by its identifier."""

	@abstractmethod
	def get_by_name(self, name: str) -> Role | None:
		"""Return one role aggregate by its unique name."""

	@abstractmethod
	def list(self) -> Sequence[Role]:
		"""Return all roles ordered for presentation."""

	@abstractmethod
	def assign_functionality(self, role_id: int, functionality_id: int) -> None:
		"""Attach a functionality to a role if the association does not already exist."""

	@abstractmethod
	def remove_functionality(self, role_id: int, functionality_id: int) -> None:
		"""Detach a functionality from a role if the association exists."""

	@abstractmethod
	def delete(self, role_id: int) -> None:
		"""Delete one role aggregate by identifier."""


class FunctionalityRepository(ABC):
	"""Contract for persisting and retrieving IAM functionalities."""

	@abstractmethod
	def add(self, functionality: Functionality) -> Functionality:
		"""Persist a new functionality and return its current state."""

	@abstractmethod
	def update(self, functionality: Functionality) -> Functionality:
		"""Persist scalar changes for an existing functionality."""

	@abstractmethod
	def get_by_id(self, functionality_id: int) -> Functionality | None:
		"""Return one functionality by its identifier."""

	@abstractmethod
	def get_by_code(self, code: str) -> Functionality | None:
		"""Return one functionality by its business code."""

	@abstractmethod
	def list(self) -> Sequence[Functionality]:
		"""Return all functionalities ordered for presentation."""

	@abstractmethod
	def delete(self, functionality_id: int) -> None:
		"""Delete one functionality by identifier."""


class RefreshTokenRepository(ABC):
	"""Contract for persisting and retrieving IAM refresh tokens."""

	@abstractmethod
	def add(self, token: RefreshToken) -> RefreshToken:
		"""Persist a new refresh token and return its current state."""

	@abstractmethod
	def get_by_jti(self, jti: str) -> RefreshToken | None:
		"""Return one refresh token by token identifier."""

	@abstractmethod
	def revoke(self, jti: str) -> None:
		"""Mark one refresh token as revoked when it exists."""
