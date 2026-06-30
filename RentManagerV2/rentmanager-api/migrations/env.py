"""
Alembic migration environment configuration.

This module configures Alembic for automatic schema migrations using SQLAlchemy models
as the source of truth. It supports both offline (SQL script generation) and online
(direct database execution) migration modes.
"""

from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ============================================================================
# PATH CONFIGURATION
# ============================================================================
# Resolve the base directory (migrations/) and add src/ to Python path
# so that application modules can be imported for metadata introspection.
BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
	sys.path.append(str(SRC_DIR))

# ============================================================================
# IMPORTS & CONFIGURATION
# ============================================================================
# Import application settings and SQLAlchemy models to access the metadata
# that defines the current state of the database schema.
from rentmanager.config import get_settings


from rentmanager.modules.finance.infrastructure.models import ExpenseTypesModel
from rentmanager.modules.finance.infrastructure.models import IncomeTypesModel
from rentmanager.modules.finance.infrastructure.models import TaxTypesModel
from rentmanager.modules.finance.infrastructure.models import PaymentsModel
from rentmanager.modules.finance.infrastructure.models import ExpenseModel
from rentmanager.modules.finance.infrastructure.models import IncomeModel
from rentmanager.modules.finance.infrastructure.models import InvoiceModel
from rentmanager.modules.finance.infrastructure.models import InvoiceLineModel
from rentmanager.modules.finance.infrastructure.models import InvoiceDocumentModel
from rentmanager.modules.finance.infrastructure.models import PaymentAttachmentModel


from rentmanager.modules.contracts.infrastructure.models import ContractDocumentModel
from rentmanager.modules.contracts.infrastructure.models import ContractModel
from rentmanager.modules.contracts.infrastructure.models import TenantContractModel
from rentmanager.modules.assets.infrastructure.models import AssetModel
from rentmanager.modules.iam.infrastructure.models import UserModel
from rentmanager.shared_kernel.infrastructure.db.base import Base

# Load Alembic configuration from alembic.ini
config = context.config
settings = get_settings()

# Override the database URL from environment settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configure logging from the alembic.ini file if specified
if config.config_file_name is not None:
	fileConfig(config.config_file_name)

# ============================================================================
# MIGRATION TARGET METADATA
# ============================================================================
# Use shared SQLAlchemy metadata as the source of truth.
# Importing each module model registers its tables into Base.metadata.
target_metadata = Base.metadata


# ============================================================================
# OFFLINE MIGRATION MODE
# ============================================================================
def run_migrations_offline() -> None:
	"""
	Run migrations in offline mode.
	
	This generates SQL migration scripts without connecting to the database.
	Useful for code review, SQL inspection, and generating migration files
	for manual execution or in CI/CD pipelines.
	"""
	url = config.get_main_option("sqlalchemy.url")
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={"paramstyle": "named"},
		compare_type=True,
	)

	with context.begin_transaction():
		context.run_migrations()


# ============================================================================
# ONLINE MIGRATION MODE
# ============================================================================
def run_migrations_online() -> None:
	"""
	Run migrations in online mode.
	
	This connects to the database and executes migration operations directly.
	Used during local development and deployment to apply schema changes
	to a live database.
	"""
	connectable = engine_from_config(
		config.get_section(config.config_ini_section, {}),
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			compare_type=True,
		)

		with context.begin_transaction():
			context.run_migrations()


# ============================================================================
# EXECUTION ENTRYPOINT
# ============================================================================
# Determine which migration mode to use based on the Alembic context.
# Offline mode is typically triggered with: alembic upgrade head --sql
# Online mode is the default: alembic upgrade head
if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
