from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rentmanager.shared_kernel.infrastructure.db.base import Base

if TYPE_CHECKING:
	from rentmanager.modules.contracts.infrastructure.models import ContractModel
	from rentmanager.modules.finance.infrastructure.models import ExpenseModel
	from rentmanager.modules.finance.infrastructure.models import IncomeModel
	from rentmanager.modules.finance.infrastructure.models import InvoiceModel
	from rentmanager.modules.finance.infrastructure.models import PaymentsModel


class AssetModel(Base):
	__tablename__ = "assets"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	asset_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	asset_type: Mapped[str] = mapped_column(String(100), nullable=False)
	name: Mapped[str] = mapped_column(String(150), nullable=False)
	address_line: Mapped[str] = mapped_column(String(255), nullable=False)
	bedroom_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
	rental_value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
	balance_favor: Mapped[Decimal] = mapped_column(
		Numeric(10, 2),
		nullable=False,
		server_default="0",
	)
	status: Mapped[str] = mapped_column(
		String(50),
		nullable=False,
		server_default="available",
	)
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

	contracts: Mapped[list["ContractModel"]] = relationship(
		back_populates="asset",
		cascade="all, delete-orphan",
	)
	payments: Mapped[list["PaymentsModel"]] = relationship(
		back_populates="asset",
		cascade="all, delete-orphan",
	)
	expenses: Mapped[list["ExpenseModel"]] = relationship(
		back_populates="asset",
		cascade="all, delete-orphan",
	)
	incomes: Mapped[list["IncomeModel"]] = relationship(
		back_populates="asset",
		cascade="all, delete-orphan",
	)
	invoices: Mapped[list["InvoiceModel"]] = relationship(
		back_populates="asset",
		cascade="all, delete-orphan",
	)