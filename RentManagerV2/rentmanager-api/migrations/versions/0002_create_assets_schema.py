"""create assets schema

Revision ID: 0002_create_assets_schema
Revises: 0001_create_iam_schema
Create Date: 2026-06-27 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_create_assets_schema"
down_revision: Union[str, None] = "0001_create_iam_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		"assets",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("asset_code", sa.String(length=50), nullable=False),
		sa.Column("asset_type", sa.String(length=100), nullable=False),
		sa.Column("name", sa.String(length=150), nullable=False),
		sa.Column("address_line", sa.String(length=255), nullable=False),
		sa.Column("bedroom_count", sa.Integer(), nullable=True),
		sa.Column("rental_value", sa.Numeric(precision=10, scale=2), nullable=False),
		sa.Column(
			"balance_favor",
			sa.Numeric(precision=10, scale=2),
			server_default=sa.text("0"),
			nullable=False,
		),
		sa.Column(
			"status",
			sa.String(length=50),
			server_default=sa.text("'available'"),
			nullable=False,
		),
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
		sa.PrimaryKeyConstraint("id", name=op.f("pk_assets")),
		sa.UniqueConstraint("asset_code", name=op.f("uq_assets_asset_code")),
	)



def downgrade() -> None:
	op.drop_table("assets")
