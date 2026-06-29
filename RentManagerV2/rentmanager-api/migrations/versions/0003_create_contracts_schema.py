"""create contracts schema

Revision ID: 0003_create_contracts_schema
Revises: 0002_create_assets_schema
Create Date: 2026-06-28 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_create_contracts_schema"
down_revision: Union[str, None] = "0002_create_assets_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		"contracts",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("contract_code", sa.String(length=50), nullable=False),
		sa.Column("asset_id", sa.Integer(), nullable=False),
		sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
		sa.Column("end_date", sa.DateTime(timezone=True), nullable=False),
		sa.Column("rent_amount", sa.Numeric(precision=10, scale=2), nullable=False),
		sa.Column("deposit_amount", sa.Numeric(precision=10, scale=2), nullable=False),
		sa.Column(
			"status",
			sa.String(length=50),
			server_default=sa.text("'active'"),
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
		sa.PrimaryKeyConstraint("id", name=op.f("pk_contracts")),
		sa.ForeignKeyConstraint(
			["asset_id"],
			["assets.id"],
			ondelete="CASCADE",
			name=op.f("fk_contracts_asset_id_assets"),
		),
		sa.UniqueConstraint("contract_code", name=op.f("uq_contracts_contract_code")),
	)

	op.create_table(
		"tenant_contracts",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("contract_id", sa.Integer(), nullable=False),
		sa.Column("user_id", sa.Integer(), nullable=False),
		sa.Column("role_in_contract", sa.String(length=50), nullable=False),
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
		sa.ForeignKeyConstraint(
			["contract_id"],
			["contracts.id"],
			ondelete="CASCADE",
			name=op.f("fk_tenant_contracts_contract_id_contracts"),
		),
		sa.ForeignKeyConstraint(
			["user_id"],
			["iam_users.id"],
			ondelete="CASCADE",
			name=op.f("fk_tenant_contracts_user_id_iam_users"),
		),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_tenant_contracts")),
		sa.UniqueConstraint("contract_id", "user_id", name="uq_tenant_contracts_contract_user"),
	)

	op.create_table(
		"contract_documents",
		sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
		sa.Column("contract_id", sa.Integer(), nullable=False),
		sa.Column("category", sa.String(length=50), nullable=False),
		sa.Column("original_filename", sa.String(length=255), nullable=False),
		sa.Column("content_type", sa.String(length=100), nullable=False),
		sa.Column("size_bytes", sa.Integer(), nullable=False),
		sa.Column("blob_container", sa.String(length=100), nullable=False),
		sa.Column("blob_key", sa.String(length=255), nullable=False),
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
		sa.ForeignKeyConstraint(
			["contract_id"],
			["contracts.id"],
			ondelete="CASCADE",
			name=op.f("fk_contract_documents_contract_id_contracts"),
		),
		sa.PrimaryKeyConstraint("id", name=op.f("pk_contract_documents")),
	)


def downgrade() -> None:
	op.drop_table("contract_documents")
	op.drop_table("tenant_contracts")
	op.drop_table("contracts")