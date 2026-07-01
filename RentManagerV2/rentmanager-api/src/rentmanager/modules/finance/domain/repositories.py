from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from rentmanager.modules.finance.domain.entities import Expense
from rentmanager.modules.finance.domain.entities import ExpenseType
from rentmanager.modules.finance.domain.entities import Income
from rentmanager.modules.finance.domain.entities import IncomeType
from rentmanager.modules.finance.domain.entities import Invoice
from rentmanager.modules.finance.domain.entities import InvoiceDocument
from rentmanager.modules.finance.domain.entities import InvoiceLine
from rentmanager.modules.finance.domain.entities import Payment
from rentmanager.modules.finance.domain.entities import PaymentAttachment
from rentmanager.modules.finance.domain.entities import TaxType


class ExpenseTypeRepository(ABC):
	"""Contract for persisting and retrieving expense type catalogs."""

	@abstractmethod
	def add(self, expense_type: ExpenseType) -> ExpenseType:
		"""Persist a new expense type and return its current state."""

	@abstractmethod
	def update(self, expense_type: ExpenseType) -> ExpenseType:
		"""Persist scalar changes for an existing expense type."""

	@abstractmethod
	def get_by_id(self, expense_type_id: int) -> ExpenseType | None:
		"""Return one expense type by identifier."""

	@abstractmethod
	def get_by_name(self, name: str) -> ExpenseType | None:
		"""Return one expense type by unique name."""

	@abstractmethod
	def list(self) -> Sequence[ExpenseType]:
		"""Return all expense types ordered for presentation."""

	@abstractmethod
	def delete(self, expense_type_id: int) -> None:
		"""Delete one expense type by identifier."""


class IncomeTypeRepository(ABC):
	"""Contract for persisting and retrieving income type catalogs."""

	@abstractmethod
	def add(self, income_type: IncomeType) -> IncomeType:
		"""Persist a new income type and return its current state."""

	@abstractmethod
	def update(self, income_type: IncomeType) -> IncomeType:
		"""Persist scalar changes for an existing income type."""

	@abstractmethod
	def get_by_id(self, income_type_id: int) -> IncomeType | None:
		"""Return one income type by identifier."""

	@abstractmethod
	def get_by_name(self, name: str) -> IncomeType | None:
		"""Return one income type by unique name."""

	@abstractmethod
	def list(self) -> Sequence[IncomeType]:
		"""Return all income types ordered for presentation."""

	@abstractmethod
	def delete(self, income_type_id: int) -> None:
		"""Delete one income type by identifier."""


class TaxTypeRepository(ABC):
	"""Contract for persisting and retrieving tax type catalogs."""

	@abstractmethod
	def add(self, tax_type: TaxType) -> TaxType:
		"""Persist a new tax type and return its current state."""

	@abstractmethod
	def update(self, tax_type: TaxType) -> TaxType:
		"""Persist scalar changes for an existing tax type."""

	@abstractmethod
	def get_by_id(self, tax_type_id: int) -> TaxType | None:
		"""Return one tax type by identifier."""

	@abstractmethod
	def get_by_name(self, name: str) -> TaxType | None:
		"""Return one tax type by unique name."""

	@abstractmethod
	def list(self) -> Sequence[TaxType]:
		"""Return all tax types ordered for presentation."""

	@abstractmethod
	def delete(self, tax_type_id: int) -> None:
		"""Delete one tax type by identifier."""


class PaymentRepository(ABC):
	"""Contract for persisting and retrieving payment transactions."""

	@abstractmethod
	def add(self, payment: Payment) -> Payment:
		"""Persist a new payment transaction and return its current state."""

	@abstractmethod
	def update(self, payment: Payment) -> Payment:
		"""Persist scalar changes for an existing payment transaction."""

	@abstractmethod
	def get_by_id(self, payment_id: int) -> Payment | None:
		"""Return one payment transaction by identifier."""

	@abstractmethod
	def list_by_asset(self, asset_id: int) -> Sequence[Payment]:
		"""Return payment transactions linked to one asset."""

	@abstractmethod
	def add_attachment(self, attachment: PaymentAttachment) -> PaymentAttachment:
		"""Attach one evidence metadata record to a payment."""

	@abstractmethod
	def remove_attachment(self, attachment_id: int) -> None:
		"""Delete one payment evidence metadata record by identifier."""

	@abstractmethod
	def delete(self, payment_id: int) -> None:
		"""Delete one payment transaction by identifier."""


class ExpenseRepository(ABC):
	"""Contract for persisting and retrieving expense transactions."""

	@abstractmethod
	def add(self, expense: Expense) -> Expense:
		"""Persist a new expense transaction and return its current state."""

	@abstractmethod
	def update(self, expense: Expense) -> Expense:
		"""Persist scalar changes for an existing expense transaction."""

	@abstractmethod
	def get_by_id(self, expense_id: int) -> Expense | None:
		"""Return one expense transaction by identifier."""

	@abstractmethod
	def list_by_asset(self, asset_id: int) -> Sequence[Expense]:
		"""Return expense transactions linked to one asset."""

	@abstractmethod
	def delete(self, expense_id: int) -> None:
		"""Delete one expense transaction by identifier."""


class IncomeRepository(ABC):
	"""Contract for persisting and retrieving income transactions."""

	@abstractmethod
	def add(self, income: Income) -> Income:
		"""Persist a new income transaction and return its current state."""

	@abstractmethod
	def update(self, income: Income) -> Income:
		"""Persist scalar changes for an existing income transaction."""

	@abstractmethod
	def get_by_id(self, income_id: int) -> Income | None:
		"""Return one income transaction by identifier."""

	@abstractmethod
	def list_by_asset(self, asset_id: int) -> Sequence[Income]:
		"""Return income transactions linked to one asset."""

	@abstractmethod
	def delete(self, income_id: int) -> None:
		"""Delete one income transaction by identifier."""


class InvoiceRepository(ABC):
	"""Contract for persisting and retrieving invoice aggregates."""

	@abstractmethod
	def add(self, invoice: Invoice) -> Invoice:
		"""Persist a new invoice aggregate and return its current state."""

	@abstractmethod
	def update(self, invoice: Invoice) -> Invoice:
		"""Persist scalar changes for an existing invoice aggregate."""

	@abstractmethod
	def get_by_id(self, invoice_id: int) -> Invoice | None:
		"""Return one invoice aggregate by identifier."""

	@abstractmethod
	def list_by_asset(self, asset_id: int) -> Sequence[Invoice]:
		"""Return invoice aggregates linked to one asset."""

	@abstractmethod
	def add_line(self, line: InvoiceLine) -> InvoiceLine:
		"""Attach one line item to an invoice."""

	@abstractmethod
	def remove_line(self, line_id: int) -> None:
		"""Delete one invoice line item by identifier."""

	@abstractmethod
	def add_document(self, document: InvoiceDocument) -> InvoiceDocument:
		"""Attach one document metadata record to an invoice."""

	@abstractmethod
	def remove_document(self, document_id: int) -> None:
		"""Delete one invoice document metadata record by identifier."""

	@abstractmethod
	def delete(self, invoice_id: int) -> None:
		"""Delete one invoice aggregate by identifier."""
