"""create finance schema

Revision ID: 0004_create_finance_schema
Revises: 0003_create_contracts_schema
Create Date: 2026-06-28 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_create_finance_schema"
down_revision: Union[str, None] = "0003_create_contracts_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "expense_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_expense_types")),
        sa.UniqueConstraint("name", name=op.f("uq_expense_types_name")),
    )

    op.create_table(
        "income_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_income_types")),
        sa.UniqueConstraint("name", name=op.f("uq_income_types_name")),
    )

    op.create_table(
        "tax_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("tax_percentage", sa.Numeric(precision=5, scale=2), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tax_types")),
        sa.UniqueConstraint("name", name=op.f("uq_tax_types_name")),
    )

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("bank_reference", sa.String(length=100), nullable=True),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
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
            ["asset_id"],
            ["assets.id"],
            ondelete="CASCADE",
            name=op.f("fk_payments_asset_id_assets"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payments")),
    )

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("expense_type_id", sa.Integer(), nullable=False),
        sa.Column("payment_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("deductible", sa.Boolean(), server_default=sa.text("0"), nullable=False),
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
            ["asset_id"],
            ["assets.id"],
            ondelete="CASCADE",
            name=op.f("fk_expenses_asset_id_assets"),
        ),
        sa.ForeignKeyConstraint(
            ["expense_type_id"],
            ["expense_types.id"],
            name=op.f("fk_expenses_expense_type_id_expense_types"),
        ),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payments.id"],
            ondelete="SET NULL",
            name=op.f("fk_expenses_payment_id_payments"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_expenses")),
    )

    op.create_table(
        "incomes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("income_type_id", sa.Integer(), nullable=False),
        sa.Column("payment_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
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
            ["asset_id"],
            ["assets.id"],
            ondelete="CASCADE",
            name=op.f("fk_incomes_asset_id_assets"),
        ),
        sa.ForeignKeyConstraint(
            ["income_type_id"],
            ["income_types.id"],
            name=op.f("fk_incomes_income_type_id_income_types"),
        ),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payments.id"],
            ondelete="SET NULL",
            name=op.f("fk_incomes_payment_id_payments"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_incomes")),
    )

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
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
            ["asset_id"],
            ["assets.id"],
            ondelete="CASCADE",
            name=op.f("fk_invoices_asset_id_assets"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoices")),
    )

    op.create_table(
        "invoice_lines",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=False),
        sa.Column("expense_id", sa.Integer(), nullable=True),
        sa.Column("income_id", sa.Integer(), nullable=True),
        sa.Column("line_type", sa.String(length=50), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
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
        sa.CheckConstraint(
            "((expense_id IS NOT NULL AND income_id IS NULL AND line_type = 'expense') OR "
            "(expense_id IS NULL AND income_id IS NOT NULL AND line_type = 'income'))",
            name="ck_invoice_lines_reference_matches_type",
        ),
        sa.ForeignKeyConstraint(
            ["expense_id"],
            ["expenses.id"],
            ondelete="CASCADE",
            name=op.f("fk_invoice_lines_expense_id_expenses"),
        ),
        sa.ForeignKeyConstraint(
            ["income_id"],
            ["incomes.id"],
            ondelete="CASCADE",
            name=op.f("fk_invoice_lines_income_id_incomes"),
        ),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["invoices.id"],
            ondelete="CASCADE",
            name=op.f("fk_invoice_lines_invoice_id_invoices"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoice_lines")),
    )

    op.create_table(
        "payment_attachments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("payment_id", sa.Integer(), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("blob_container", sa.String(length=100), nullable=False),
        sa.Column("blob_key", sa.String(length=255), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payments.id"],
            ondelete="CASCADE",
            name=op.f("fk_payment_attachments_payment_id_payments"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payment_attachments")),
    )

    op.create_table(
        "invoice_documents",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("blob_container", sa.String(length=100), nullable=False),
        sa.Column("blob_key", sa.String(length=255), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["invoices.id"],
            ondelete="CASCADE",
            name=op.f("fk_invoice_documents_invoice_id_invoices"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoice_documents")),
    )

def downgrade() -> None:
    op.drop_table("invoice_documents")
    op.drop_table("payment_attachments")
    op.drop_table("invoice_lines")
    op.drop_table("invoices")
    op.drop_table("incomes")
    op.drop_table("expenses")
    op.drop_table("payments")
    op.drop_table("tax_types")
    op.drop_table("income_types")
    op.drop_table("expense_types")
