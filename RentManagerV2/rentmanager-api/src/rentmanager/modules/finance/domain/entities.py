from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class ExpenseType:
	"""Domain representation of an expense category."""

	id: int | None
	name: str
	description: str | None = None


@dataclass(slots=True)
class IncomeType:
	"""Domain representation of an income category."""

	id: int | None
	name: str
	description: str | None = None


@dataclass(slots=True)
class TaxType:
	"""Domain representation of a tax category."""

	id: int | None
	name: str
	description: str | None
	tax_percentage: Decimal


@dataclass(slots=True)
class PaymentAttachment:
	"""Domain representation of payment evidence metadata."""

	id: int | None
	payment_id: int
	original_filename: str
	content_type: str
	size_bytes: int
	blob_container: str
	blob_key: str
	uploaded_at: datetime | None = None


@dataclass(slots=True)
class Payment:
	"""Domain representation of a payment transaction."""

	id: int | None
	asset_id: int
	registered_at: datetime
	bank_reference: str | None
	amount: Decimal
	description: str | None
	status: str
	created_at: datetime | None = None
	updated_at: datetime | None = None
	attachments: list[PaymentAttachment] = field(default_factory=list)


@dataclass(slots=True)
class Expense:
	"""Domain representation of an expense transaction."""

	id: int | None
	asset_id: int
	expense_type_id: int
	payment_id: int | None
	amount: Decimal
	registered_at: datetime
	description: str | None
	deductible: bool
	created_at: datetime | None = None
	updated_at: datetime | None = None


@dataclass(slots=True)
class Income:
	"""Domain representation of an income transaction."""

	id: int | None
	asset_id: int
	income_type_id: int
	payment_id: int | None
	amount: Decimal
	registered_at: datetime
	description: str | None
	created_at: datetime | None = None
	updated_at: datetime | None = None


@dataclass(slots=True)
class InvoiceLine:
	"""Domain representation of one invoice line item."""

	id: int | None
	invoice_id: int
	expense_id: int | None
	income_id: int | None
	line_type: str
	amount: Decimal
	created_at: datetime | None = None
	updated_at: datetime | None = None


@dataclass(slots=True)
class InvoiceDocument:
	"""Domain representation of invoice document metadata."""

	id: int | None
	invoice_id: int
	original_filename: str
	content_type: str
	size_bytes: int
	blob_container: str
	blob_key: str
	uploaded_at: datetime | None = None


@dataclass(slots=True)
class Invoice:
	"""Domain representation of an invoice aggregate."""

	id: int | None
	asset_id: int
	issued_at: datetime
	total_amount: Decimal
	status: str
	created_at: datetime | None = None
	updated_at: datetime | None = None
	lines: list[InvoiceLine] = field(default_factory=list)
	documents: list[InvoiceDocument] = field(default_factory=list)
