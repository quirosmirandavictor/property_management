from __future__ import annotations

import os
import sys

from sqlalchemy import select

from rentmanager.modules.iam.infrastructure.models import FunctionalityModel
from rentmanager.modules.iam.infrastructure.models import RoleModel
from rentmanager.modules.iam.infrastructure.models import RoleFunctionalityModel
from rentmanager.modules.iam.infrastructure.models import UserModel
from rentmanager.modules.iam.infrastructure.models import UserRoleModel
from rentmanager.shared_kernel.infrastructure.db.session import SessionFactory
from rentmanager.shared_kernel.infrastructure.security.password_hasher import PasswordHasher


def _get_env(name: str, default: str) -> str:
	value = os.getenv(name, default).strip()
	if not value:
		raise ValueError(f"Environment variable {name} cannot be empty.")
	return value


def main() -> int:
	username = _get_env("IAM_ADMIN_USERNAME", "admin")
	password = _get_env("IAM_ADMIN_PASSWORD", "Admin123*")
	first_name = _get_env("IAM_ADMIN_FIRST_NAME", "System")
	last_name = _get_env("IAM_ADMIN_LAST_NAME", "Administrator")
	email = _get_env("IAM_ADMIN_EMAIL", "admin@local.dev")
	role_name = _get_env("IAM_ADMIN_ROLE", "ADMIN")
	functionalities = {
		"assets.read": ("Read assets", "Allow querying asset information"),
		"assets.write": ("Write assets", "Allow creating and mutating asset information"),
	}

	if len(password) < 6:
		print("IAM_ADMIN_PASSWORD must be at least 6 characters long.", file=sys.stderr)
		return 1

	session = SessionFactory()
	password_hasher = PasswordHasher()

	try:
		role = session.scalar(select(RoleModel).where(RoleModel.name == role_name))
		role_created = False
		if role is None:
			role = RoleModel(name=role_name, description="Bootstrap admin role")
			session.add(role)
			session.flush()
			role_created = True

		user = session.scalar(select(UserModel).where(UserModel.username == username))
		user_created = False
		if user is None:
			user = UserModel(
				dni=None,
				username=username,
				first_name=first_name,
				last_name=last_name,
				email=email,
				phone=None,
				password_hash=password_hasher.hash(password),
				is_active=True,
			)
			session.add(user)
			session.flush()
			user_created = True
		elif not user.is_active:
			user.is_active = True

		assignment = session.scalar(
			select(UserRoleModel).where(
				UserRoleModel.user_id == user.id,
				UserRoleModel.role_id == role.id,
			)
		)
		role_linked = False
		if assignment is None:
			session.add(UserRoleModel(user_id=user.id, role_id=role.id))
			role_linked = True

		functionalities_created = 0
		functionalities_linked = 0
		for functionality_code, (functionality_name, functionality_description) in functionalities.items():
			functionality = session.scalar(
				select(FunctionalityModel).where(FunctionalityModel.code == functionality_code)
			)
			if functionality is None:
				functionality = FunctionalityModel(
					code=functionality_code,
					name=functionality_name,
					description=functionality_description,
				)
				session.add(functionality)
				session.flush()
				functionalities_created += 1

			role_functionality = session.scalar(
				select(RoleFunctionalityModel).where(
					RoleFunctionalityModel.role_id == role.id,
					RoleFunctionalityModel.functionality_id == functionality.id,
				)
			)
			if role_functionality is None:
				session.add(
					RoleFunctionalityModel(role_id=role.id, functionality_id=functionality.id)
				)
				functionalities_linked += 1

		session.commit()

		print(
			"Bootstrap admin completed "
			f"(user_created={user_created}, role_created={role_created}, role_linked={role_linked}, "
			f"functionalities_created={functionalities_created}, functionalities_linked={functionalities_linked})."
		)
		return 0
	except Exception as exc:
		session.rollback()
		print(f"Bootstrap admin failed: {exc}", file=sys.stderr)
		return 1
	finally:
		session.close()


if __name__ == "__main__":
	raise SystemExit(main())
