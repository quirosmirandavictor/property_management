from __future__ import annotations

from rentmanager.modules.iam.domain.entities import Functionality
from rentmanager.modules.iam.domain.entities import Role
from rentmanager.modules.iam.domain.entities import User
from rentmanager.modules.iam.infrastructure.models import FunctionalityModel
from rentmanager.modules.iam.infrastructure.models import RoleModel
from rentmanager.modules.iam.infrastructure.models import UserModel


def functionality_to_entity(model: FunctionalityModel) -> Functionality:
	"""Translate one ORM functionality row into a domain entity."""

	return Functionality(
		id=model.id,
		code=model.code,
		name=model.name,
		description=model.description,
	)


def role_to_entity(model: RoleModel) -> Role:
	"""Translate one ORM role row into a domain aggregate."""

	functionalities = [
		functionality_to_entity(assignment.functionality)
		for assignment in model.functionalities
		if assignment.functionality is not None
	]

	return Role(
		id=model.id,
		name=model.name,
		description=model.description,
		functionalities=functionalities,
	)


def user_to_entity(model: UserModel) -> User:
	"""Translate one ORM user row into a domain aggregate."""

	roles = [
		role_to_entity(assignment.role)
		for assignment in model.roles
		if assignment.role is not None
	]

	return User(
		id=model.id,
		dni=model.dni,
		username=model.username,
		first_name=model.first_name,
		last_name=model.last_name,
		email=model.email,
		phone=model.phone,
		password_hash=model.password_hash,
		is_active=model.is_active,
		created_at=model.created_at,
		updated_at=model.updated_at,
		roles=roles,
	)


def merge_functionality_into_model(
	entity: Functionality,
	model: FunctionalityModel | None = None,
) -> FunctionalityModel:
	"""Copy scalar domain fields into an ORM functionality instance."""

	model = model or FunctionalityModel()
	model.code = entity.code
	model.name = entity.name
	model.description = entity.description
	return model


def merge_role_into_model(entity: Role, model: RoleModel | None = None) -> RoleModel:
	"""Copy scalar domain fields into an ORM role instance."""

	model = model or RoleModel()
	model.name = entity.name
	model.description = entity.description
	return model


def merge_user_into_model(entity: User, model: UserModel | None = None) -> UserModel:
	"""Copy scalar domain fields into an ORM user instance."""

	model = model or UserModel()
	model.dni = entity.dni
	model.username = entity.username
	model.first_name = entity.first_name
	model.last_name = entity.last_name
	model.email = entity.email
	model.phone = entity.phone
	model.password_hash = entity.password_hash
	model.is_active = entity.is_active
	return model
