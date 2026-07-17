"""extend contract documents and permissions

Revision ID: 0006_extend_contract_documents_and_permissions
Revises: 0005_create_iam_refresh_tokens
Create Date: 2026-07-16 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0006_extend_contract_documents_and_permissions"
down_revision: Union[str, None] = "0005_create_iam_refresh_tokens"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column(
		"contract_documents",
		sa.Column(
			"uploaded_at",
			sa.DateTime(timezone=True),
			nullable=False,
			server_default=sa.text("CURRENT_TIMESTAMP"),
		),
	)

	op.execute(
		sa.text(
			"""
			INSERT INTO iam_functionalities (code, name, description)
			SELECT 'contracts.read', 'Read contracts', 'Allow querying contract information'
			WHERE NOT EXISTS (
				SELECT 1 FROM iam_functionalities WHERE code = 'contracts.read'
			)
			"""
		)
	)
	op.execute(
		sa.text(
			"""
			INSERT INTO iam_functionalities (code, name, description)
			SELECT 'contracts.write', 'Write contracts', 'Allow creating and mutating contract information'
			WHERE NOT EXISTS (
				SELECT 1 FROM iam_functionalities WHERE code = 'contracts.write'
			)
			"""
		)
	)


def downgrade() -> None:
	op.execute(sa.text("DELETE FROM iam_functionalities WHERE code = 'contracts.write'"))
	op.execute(sa.text("DELETE FROM iam_functionalities WHERE code = 'contracts.read'"))
	op.drop_column("contract_documents", "uploaded_at")
