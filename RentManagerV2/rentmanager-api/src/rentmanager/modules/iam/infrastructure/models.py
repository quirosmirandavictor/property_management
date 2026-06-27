from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rentmanager.shared_kernel.infrastructure.db.base import Base


class UserModel(Base):
	__tablename__ = "iam_users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	dni: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
	username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	first_name: Mapped[str] = mapped_column(String(100), nullable=False)
	last_name: Mapped[str] = mapped_column(String(100), nullable=False)
	email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
	phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
	password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
	is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="1")
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	roles: Mapped[list[UserRoleModel]] = relationship(
		back_populates="user",
		cascade="all, delete-orphan",
	)


class RoleModel(Base):
	__tablename__ = "iam_roles"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	description: Mapped[str | None] = mapped_column(String(255), nullable=True)

	users: Mapped[list[UserRoleModel]] = relationship(
		back_populates="role",
		cascade="all, delete-orphan",
	)
	functionalities: Mapped[list[RoleFunctionalityModel]] = relationship(
		back_populates="role",
		cascade="all, delete-orphan",
	)


class FunctionalityModel(Base):
	__tablename__ = "iam_functionalities"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	description: Mapped[str | None] = mapped_column(String(255), nullable=True)

	roles: Mapped[list[RoleFunctionalityModel]] = relationship(
		back_populates="functionality",
		cascade="all, delete-orphan",
	)


class UserRoleModel(Base):
	__tablename__ = "iam_user_roles"
	__table_args__ = (
		UniqueConstraint("user_id", "role_id", name="uq_iam_user_roles_user_role"),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(
		ForeignKey("iam_users.id", ondelete="CASCADE"),
		nullable=False,
	)
	role_id: Mapped[int] = mapped_column(
		ForeignKey("iam_roles.id", ondelete="CASCADE"),
		nullable=False,
	)

	user: Mapped[UserModel] = relationship(back_populates="roles")
	role: Mapped[RoleModel] = relationship(back_populates="users")


class RoleFunctionalityModel(Base):
	__tablename__ = "iam_role_functionalities"
	__table_args__ = (
		UniqueConstraint(
			"role_id",
			"functionality_id",
			name="uq_iam_role_functionalities_role_functionality",
		),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	role_id: Mapped[int] = mapped_column(
		ForeignKey("iam_roles.id", ondelete="CASCADE"),
		nullable=False,
	)
	functionality_id: Mapped[int] = mapped_column(
		ForeignKey("iam_functionalities.id", ondelete="CASCADE"),
		nullable=False,
	)

	role: Mapped[RoleModel] = relationship(back_populates="functionalities")
	functionality: Mapped[FunctionalityModel] = relationship(back_populates="roles")
