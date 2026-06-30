from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rentmanager.modules.assets.infrastructure.models import AssetModel
from rentmanager.shared_kernel.infrastructure.db.base import Base

class ExpenseTypesModel(Base):
    __tablename__ = "expense_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

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

class IncomeTypesModel(Base):
    __tablename__ = "income_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

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

class TaxTypesModel(Base):
    __tablename__ = "tax_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    tax_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

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

class PaymentsModel(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
    )
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    bank_reference: Mapped[str] = mapped_column(String(100), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    asset: Mapped["AssetModel"] = relationship("AssetModel", back_populates="payments")
    expenses: Mapped[list["ExpenseModel"]] = relationship(back_populates="payment")
    incomes: Mapped[list["IncomeModel"]] = relationship(back_populates="payment")
    attachments: Mapped[list["PaymentAttachmentModel"]] = relationship(
        back_populates="payment",
        cascade="all, delete-orphan",
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

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
    )
    expense_type_id: Mapped[int] = mapped_column(ForeignKey("expense_types.id"), nullable=False)
    payment_id: Mapped[int | None] = mapped_column(
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    deductible: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="0")

    asset: Mapped["AssetModel"] = relationship("AssetModel", back_populates="expenses")
    expense_type: Mapped["ExpenseTypesModel"] = relationship("ExpenseTypesModel")
    payment: Mapped["PaymentsModel | None"] = relationship("PaymentsModel", back_populates="expenses")
    invoice_lines: Mapped[list["InvoiceLineModel"]] = relationship(back_populates="expense")

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

class IncomeModel(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
    )
    income_type_id: Mapped[int] = mapped_column(ForeignKey("income_types.id"), nullable=False)
    payment_id: Mapped[int | None] = mapped_column(
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    asset: Mapped["AssetModel"] = relationship("AssetModel", back_populates="incomes")
    income_type: Mapped["IncomeTypesModel"] = relationship("IncomeTypesModel")
    payment: Mapped["PaymentsModel | None"] = relationship("PaymentsModel", back_populates="incomes")
    invoice_lines: Mapped[list["InvoiceLineModel"]] = relationship(back_populates="income")

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

class InvoiceModel(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
    )
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    asset: Mapped["AssetModel"] = relationship("AssetModel", back_populates="invoices")
    lines: Mapped[list["InvoiceLineModel"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
    )
    documents: Mapped[list["InvoiceDocumentModel"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
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

class InvoiceLineModel(Base):
    __tablename__ = "invoice_lines"
    __table_args__ = (
        CheckConstraint(
            "((expense_id IS NOT NULL AND income_id IS NULL AND line_type = 'expense') OR "
            "(expense_id IS NULL AND income_id IS NOT NULL AND line_type = 'income'))",
            name="ck_invoice_lines_reference_matches_type",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
    )
    expense_id: Mapped[int | None] = mapped_column(
        ForeignKey("expenses.id", ondelete="CASCADE"),
        nullable=True,
    )
    income_id: Mapped[int | None] = mapped_column(
        ForeignKey("incomes.id", ondelete="CASCADE"),
        nullable=True,
    )
    line_type: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    invoice: Mapped["InvoiceModel"] = relationship("InvoiceModel", back_populates="lines")
    expense: Mapped["ExpenseModel | None"] = relationship("ExpenseModel", back_populates="invoice_lines")
    income: Mapped["IncomeModel | None"] = relationship("IncomeModel", back_populates="invoice_lines")

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


class PaymentAttachmentModel(Base):
    __tablename__ = "payment_attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    payment_id: Mapped[int] = mapped_column(
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    blob_container: Mapped[str] = mapped_column(String(100), nullable=False)
    blob_key: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    payment: Mapped["PaymentsModel"] = relationship("PaymentsModel", back_populates="attachments")


class InvoiceDocumentModel(Base):
    __tablename__ = "invoice_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    blob_container: Mapped[str] = mapped_column(String(100), nullable=False)
    blob_key: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    invoice: Mapped["InvoiceModel"] = relationship("InvoiceModel", back_populates="documents")