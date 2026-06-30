from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from rentmanager.modules.iam.domain.entities import Functionality
from rentmanager.modules.iam.domain.entities import Role
from rentmanager.modules.iam.domain.entities import User
from rentmanager.modules.iam.domain.repositories import FunctionalityRepository
from rentmanager.modules.iam.domain.repositories import RoleRepository
from rentmanager.modules.iam.domain.repositories import UserRepository
from rentmanager.modules.iam.infrastructure.mappers import functionality_to_entity
from rentmanager.modules.iam.infrastructure.mappers import merge_functionality_into_model
from rentmanager.modules.iam.infrastructure.mappers import merge_role_into_model
from rentmanager.modules.iam.infrastructure.mappers import merge_user_into_model
from rentmanager.modules.iam.infrastructure.mappers import role_to_entity
from rentmanager.modules.iam.infrastructure.mappers import user_to_entity
from rentmanager.modules.iam.infrastructure.models import FunctionalityModel
from rentmanager.modules.iam.infrastructure.models import RoleFunctionalityModel
from rentmanager.modules.iam.infrastructure.models import RoleModel
from rentmanager.modules.iam.infrastructure.models import UserModel
from rentmanager.modules.iam.infrastructure.models import UserRoleModel


def _user_load_statement() -> tuple:
	"""Define eager-load paths required to build a full user aggregate."""

	return (
		selectinload(UserModel.roles)
		.selectinload(UserRoleModel.role)
		.selectinload(RoleModel.functionalities)
		.selectinload(RoleFunctionalityModel.functionality),
	)


def _role_load_statement() -> tuple:
	"""Define eager-load paths required to build a full role aggregate."""

	return (
		selectinload(RoleModel.functionalities).selectinload(RoleFunctionalityModel.functionality),
	)


class SqlAlchemyUserRepository(UserRepository):
	"""SQLAlchemy implementation of the IAM user repository contract."""

	def __init__(self, session: Session) -> None:
		"""Store the current SQLAlchemy session used by the unit of work."""

		self._session = session

	def add(self, user: User) -> User:
		"""Insert a new user row and return the resulting aggregate."""

		model = merge_user_into_model(user)
		self._session.add(model)
		self._session.flush()
		return user_to_entity(model)

	def update(self, user: User) -> User:
		"""Update scalar fields of an existing user row and return the aggregate."""

		model = self._require_user_model(user.id)
		merge_user_into_model(user, model)
		self._session.flush()
		return user_to_entity(model)

	def get_by_id(self, user_id: int) -> User | None:
		"""Load one user aggregate by identifier."""

		stmt = (
			select(UserModel)
			.options(*_user_load_statement())
			.where(UserModel.id == user_id)
		)
		model = self._session.scalar(stmt)
		return user_to_entity(model) if model is not None else None

	def get_by_username(self, username: str) -> User | None:
		"""Load one user aggregate by username."""

		stmt = (
			select(UserModel)
			.options(*_user_load_statement())
			.where(UserModel.username == username)
		)
		model = self._session.scalar(stmt)
		return user_to_entity(model) if model is not None else None

	def get_by_email(self, email: str) -> User | None:
		"""Load one user aggregate by email address."""

		stmt = select(UserModel).options(*_user_load_statement()).where(UserModel.email == email)
		model = self._session.scalar(stmt)
		return user_to_entity(model) if model is not None else None

	def list(self, *, is_active: bool | None = None) -> Sequence[User]:
		"""Load users with an optional activation-state filter."""

		stmt = select(UserModel).order_by(UserModel.id)
		if is_active is not None:
			stmt = stmt.where(UserModel.is_active == is_active)
		stmt = stmt.options(*_user_load_statement())
		return [user_to_entity(model) for model in self._session.scalars(stmt).all()]

	def assign_role(self, user_id: int, role_id: int) -> None:
		"""Attach one role to one user if the link does not already exist."""

		user = self._require_user_model(user_id)
		role = self._require_role_model(role_id)
		for assignment in user.roles:
			if assignment.role_id == role_id:
				return

		assignment = UserRoleModel(user=user, role=role)
		self._session.add(assignment)
		self._session.flush()

	def remove_role(self, user_id: int, role_id: int) -> None:
		"""Detach one role from one user if the link exists."""

		user = self._require_user_model(user_id)
		assignment = next((item for item in user.roles if item.role_id == role_id), None)
		if assignment is not None:
			self._session.delete(assignment)
			self._session.flush()

	def delete(self, user_id: int) -> None:
		"""Delete one user aggregate by identifier."""

		self._session.delete(self._require_user_model(user_id))

	def _require_user_model(self, user_id: int | None) -> UserModel:
		"""Resolve one user model or fail fast when the identifier is invalid."""

		if user_id is None:
			raise ValueError("User id is required for this operation.")
		model = self._session.get(UserModel, user_id)
		if model is None:
			raise ValueError(f"User with id {user_id} was not found.")
		return model

	def _require_role_model(self, role_id: int | None) -> RoleModel:
		"""Resolve one role model or fail fast when the identifier is invalid."""

		if role_id is None:
			raise ValueError("Role id is required for this operation.")
		model = self._session.get(RoleModel, role_id)
		if model is None:
			raise ValueError(f"Role with id {role_id} was not found.")
		return model


class SqlAlchemyRoleRepository(RoleRepository):
	"""SQLAlchemy implementation of the IAM role repository contract."""

	def __init__(self, session: Session) -> None:
		"""Store the current SQLAlchemy session used by the unit of work."""

		self._session = session

	def add(self, role: Role) -> Role:
		"""Insert a new role row and return the resulting aggregate."""

		model = merge_role_into_model(role)
		self._session.add(model)
		self._session.flush()
		return role_to_entity(model)

	def update(self, role: Role) -> Role:
		"""Update scalar fields of an existing role row and return the aggregate."""

		model = self._require_role_model(role.id)
		merge_role_into_model(role, model)
		self._session.flush()
		return role_to_entity(model)

	def get_by_id(self, role_id: int) -> Role | None:
		"""Load one role aggregate by identifier."""

		stmt = (
			select(RoleModel)
			.options(*_role_load_statement())
			.where(RoleModel.id == role_id)
		)
		model = self._session.scalar(stmt)
		return role_to_entity(model) if model is not None else None

	def get_by_name(self, name: str) -> Role | None:
		"""Load one role aggregate by its unique name."""

		stmt = select(RoleModel).options(*_role_load_statement()).where(RoleModel.name == name)
		model = self._session.scalar(stmt)
		return role_to_entity(model) if model is not None else None

	def list(self) -> Sequence[Role]:
		"""Load all role aggregates ordered by role name."""

		stmt = select(RoleModel).options(*_role_load_statement()).order_by(RoleModel.name)
		return [role_to_entity(model) for model in self._session.scalars(stmt).all()]

	def assign_functionality(self, role_id: int, functionality_id: int) -> None:
		"""Attach one functionality to one role if the link does not already exist."""

		role = self._require_role_model(role_id)
		functionality = self._require_functionality_model(functionality_id)
		for assignment in role.functionalities:
			if assignment.functionality_id == functionality_id:
				return

		assignment = RoleFunctionalityModel(role=role, functionality=functionality)
		self._session.add(assignment)
		self._session.flush()

	def remove_functionality(self, role_id: int, functionality_id: int) -> None:
		"""Detach one functionality from one role if the link exists."""

		role = self._require_role_model(role_id)
		assignment = next(
			(item for item in role.functionalities if item.functionality_id == functionality_id),
			None,
		)
		if assignment is not None:
			self._session.delete(assignment)
			self._session.flush()

	def delete(self, role_id: int) -> None:
		"""Delete one role aggregate by identifier."""

		self._session.delete(self._require_role_model(role_id))

	def _require_role_model(self, role_id: int | None) -> RoleModel:
		"""Resolve one role model or fail fast when the identifier is invalid."""

		if role_id is None:
			raise ValueError("Role id is required for this operation.")
		model = self._session.get(RoleModel, role_id)
		if model is None:
			raise ValueError(f"Role with id {role_id} was not found.")
		return model

	def _require_functionality_model(self, functionality_id: int | None) -> FunctionalityModel:
		"""Resolve one functionality model or fail fast when the identifier is invalid."""

		if functionality_id is None:
			raise ValueError("Functionality id is required for this operation.")
		model = self._session.get(FunctionalityModel, functionality_id)
		if model is None:
			raise ValueError(f"Functionality with id {functionality_id} was not found.")
		return model


class SqlAlchemyFunctionalityRepository(FunctionalityRepository):
	"""SQLAlchemy implementation of the IAM functionality repository contract."""

	def __init__(self, session: Session) -> None:
		"""Store the current SQLAlchemy session used by the unit of work."""

		self._session = session

	def add(self, functionality: Functionality) -> Functionality:
		"""Insert a new functionality row and return the resulting entity."""

		model = merge_functionality_into_model(functionality)
		self._session.add(model)
		self._session.flush()
		return functionality_to_entity(model)

	def update(self, functionality: Functionality) -> Functionality:
		"""Update scalar fields of an existing functionality row and return the entity."""

		model = self._require_functionality_model(functionality.id)
		merge_functionality_into_model(functionality, model)
		self._session.flush()
		return functionality_to_entity(model)

	def get_by_id(self, functionality_id: int) -> Functionality | None:
		"""Load one functionality by identifier."""

		stmt = select(FunctionalityModel).where(FunctionalityModel.id == functionality_id)
		model = self._session.scalar(stmt)
		return functionality_to_entity(model) if model is not None else None

	def get_by_code(self, code: str) -> Functionality | None:
		"""Load one functionality by business code."""

		stmt = select(FunctionalityModel).where(FunctionalityModel.code == code)
		model = self._session.scalar(stmt)
		return functionality_to_entity(model) if model is not None else None

	def list(self) -> Sequence[Functionality]:
		"""Load all functionalities ordered by code."""

		stmt = select(FunctionalityModel).order_by(FunctionalityModel.code)
		return [functionality_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, functionality_id: int) -> None:
		"""Delete one functionality by identifier."""

		self._session.delete(self._require_functionality_model(functionality_id))

	def _require_functionality_model(self, functionality_id: int | None) -> FunctionalityModel:
		"""Resolve one functionality model or fail fast when the identifier is invalid."""

		if functionality_id is None:
			raise ValueError("Functionality id is required for this operation.")
		model = self._session.get(FunctionalityModel, functionality_id)
		if model is None:
			raise ValueError(f"Functionality with id {functionality_id} was not found.")
		return model
