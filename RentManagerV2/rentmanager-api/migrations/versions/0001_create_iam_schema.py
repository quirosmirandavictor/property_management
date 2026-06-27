"""create iam schema

Revision ID: 0001_create_iam_schema
Revises:
Create Date: 2026-06-26 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_iam_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		"iam_users",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("dni", sa.String(length=50), nullable=True),
		sa.Column("username", sa.String(length=100), nullable=False),
		sa.Column("first_name", sa.String(length=100), nullable=False),
		sa.Column("last_name", sa.String(length=100), nullable=False),
		sa.Column("email", sa.String(length=254), nullable=False),
		sa.Column("phone", sa.String(length=50), nullable=True),
		sa.Column("password_hash", sa.String(length=255), nullable=False),
		sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
		sa.Column(
			"created_at",
			sa.DateTime(timezone=True),
			server_default=sa.text("CURRENT_TIMESTAMP"),
			nullable=False,
		),
		sa.Column(
			"updated_at",
			sa.DateTime(timezone=True),
			server_default=sa.text("CURRENT_TIMESTAMP"),
			nullable=False,
		),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_iam_users")),
		sa.UniqueConstraint("dni", name=op.f("uq_iam_users_dni")),
		sa.UniqueConstraint("email", name=op.f("uq_iam_users_email")),
		sa.UniqueConstraint("username", name=op.f("uq_iam_users_username")),
	)

	op.create_table(
		"iam_roles",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("name", sa.String(length=100), nullable=False),
		sa.Column("description", sa.String(length=255), nullable=True),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_iam_roles")),
		sa.UniqueConstraint("name", name=op.f("uq_iam_roles_name")),
	)

	op.create_table(
		"iam_functionalities",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("code", sa.String(length=100), nullable=False),
		sa.Column("name", sa.String(length=100), nullable=False),
		sa.Column("description", sa.String(length=255), nullable=True),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_iam_functionalities")),
		sa.UniqueConstraint("code", name=op.f("uq_iam_functionalities_code")),
	)

	op.create_table(
		"iam_user_roles",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("user_id", sa.Integer(), nullable=False),
		sa.Column("role_id", sa.Integer(), nullable=False),
		sa.ForeignKeyConstraint(
			["role_id"],
			["iam_roles.id"],
			ondelete="CASCADE",
			name=op.f("fk_iam_user_roles_role_id_iam_roles"),
		),
		sa.ForeignKeyConstraint(
			["user_id"],
			["iam_users.id"],
			ondelete="CASCADE",
			name=op.f("fk_iam_user_roles_user_id_iam_users"),
		),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_iam_user_roles")),
		sa.UniqueConstraint("user_id", "role_id", name="uq_iam_user_roles_user_role"),
	)

	op.create_table(
		"iam_role_functionalities",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("role_id", sa.Integer(), nullable=False),
		sa.Column("functionality_id", sa.Integer(), nullable=False),
		sa.ForeignKeyConstraint(
			["functionality_id"],
			["iam_functionalities.id"],
			ondelete="CASCADE",
			name=op.f("fk_iam_role_functionalities_functionality_id_iam_functionalities"),
		),
		sa.ForeignKeyConstraint(
			["role_id"],
			["iam_roles.id"],
			ondelete="CASCADE",
			name=op.f("fk_iam_role_functionalities_role_id_iam_roles"),
		),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_iam_role_functionalities")),
		sa.UniqueConstraint(
			"role_id",
			"functionality_id",
			name="uq_iam_role_functionalities_role_functionality",
		),
	)


def downgrade() -> None:
	op.drop_table("iam_role_functionalities")
	op.drop_table("iam_user_roles")
	op.drop_table("iam_functionalities")
	op.drop_table("iam_roles")
	op.drop_table("iam_users")