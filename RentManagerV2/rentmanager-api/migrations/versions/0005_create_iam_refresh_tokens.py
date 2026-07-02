"""create iam refresh tokens table

Revision ID: 0005_create_iam_refresh_tokens
Revises: 0004_create_finance_schema
Create Date: 2026-07-02 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0005_create_iam_refresh_tokens"
down_revision: Union[str, None] = "0004_create_finance_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		"iam_refresh_tokens",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("user_id", sa.Integer(), nullable=False),
		sa.Column("jti", sa.String(length=64), nullable=False),
		sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
		sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
		sa.Column(
			"created_at",
			sa.DateTime(timezone=True),
			server_default=sa.text("CURRENT_TIMESTAMP"),
			nullable=False,
		),
		sa.ForeignKeyConstraint(
			["user_id"],
			["iam_users.id"],
			ondelete="CASCADE",
			name=op.f("fk_iam_refresh_tokens_user_id_iam_users"),
		),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_iam_refresh_tokens")),
		sa.UniqueConstraint("jti", name=op.f("uq_iam_refresh_tokens_jti")),
	)


def downgrade() -> None:
	op.drop_table("iam_refresh_tokens")