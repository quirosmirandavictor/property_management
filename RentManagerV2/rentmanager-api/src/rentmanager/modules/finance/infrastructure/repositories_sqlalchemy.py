from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

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
from rentmanager.modules.finance.domain.repositories import ExpenseRepository
from rentmanager.modules.finance.domain.repositories import ExpenseTypeRepository
from rentmanager.modules.finance.domain.repositories import IncomeRepository
from rentmanager.modules.finance.domain.repositories import IncomeTypeRepository
from rentmanager.modules.finance.domain.repositories import InvoiceRepository
from rentmanager.modules.finance.domain.repositories import PaymentRepository
from rentmanager.modules.finance.domain.repositories import TaxTypeRepository
from rentmanager.modules.finance.infrastructure.mappers import expense_to_entity
from rentmanager.modules.finance.infrastructure.mappers import expense_type_to_entity
from rentmanager.modules.finance.infrastructure.mappers import income_to_entity
from rentmanager.modules.finance.infrastructure.mappers import income_type_to_entity
from rentmanager.modules.finance.infrastructure.mappers import invoice_document_to_entity
from rentmanager.modules.finance.infrastructure.mappers import invoice_line_to_entity
from rentmanager.modules.finance.infrastructure.mappers import invoice_to_entity
from rentmanager.modules.finance.infrastructure.mappers import merge_expense_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_expense_type_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_income_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_income_type_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_invoice_document_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_invoice_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_invoice_line_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_payment_attachment_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_payment_into_model
from rentmanager.modules.finance.infrastructure.mappers import merge_tax_type_into_model
from rentmanager.modules.finance.infrastructure.mappers import payment_attachment_to_entity
from rentmanager.modules.finance.infrastructure.mappers import payment_to_entity
from rentmanager.modules.finance.infrastructure.mappers import tax_type_to_entity
from rentmanager.modules.finance.infrastructure.models import ExpenseModel
from rentmanager.modules.finance.infrastructure.models import ExpenseTypesModel
from rentmanager.modules.finance.infrastructure.models import IncomeModel
from rentmanager.modules.finance.infrastructure.models import IncomeTypesModel
from rentmanager.modules.finance.infrastructure.models import InvoiceDocumentModel
from rentmanager.modules.finance.infrastructure.models import InvoiceLineModel
from rentmanager.modules.finance.infrastructure.models import InvoiceModel
from rentmanager.modules.finance.infrastructure.models import PaymentAttachmentModel
from rentmanager.modules.finance.infrastructure.models import PaymentsModel
from rentmanager.modules.finance.infrastructure.models import TaxTypesModel


class SqlAlchemyExpenseTypeRepository(ExpenseTypeRepository):
	"""SQLAlchemy repository for expense type catalog rows."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, expense_type: ExpenseType) -> ExpenseType:
		"""Insert a new expense type row and return the persisted entity."""

		model = merge_expense_type_into_model(expense_type)
		self._session.add(model)
		self._session.flush()
		return expense_type_to_entity(model)

	def update(self, expense_type: ExpenseType) -> ExpenseType:
		"""Persist scalar field changes for an existing expense type."""

		model = self._require_model(expense_type.id)
		merge_expense_type_into_model(expense_type, model)
		self._session.flush()
		return expense_type_to_entity(model)

	def get_by_id(self, expense_type_id: int) -> ExpenseType | None:
		"""Load one expense type row by identifier."""

		stmt = select(ExpenseTypesModel).where(ExpenseTypesModel.id == expense_type_id)
		model = self._session.scalar(stmt)
		return expense_type_to_entity(model) if model is not None else None

	def get_by_name(self, name: str) -> ExpenseType | None:
		"""Load one expense type row by its unique name."""

		stmt = select(ExpenseTypesModel).where(ExpenseTypesModel.name == name)
		model = self._session.scalar(stmt)
		return expense_type_to_entity(model) if model is not None else None

	def list(self) -> Sequence[ExpenseType]:
		"""Load all expense type rows ordered by name."""

		stmt = select(ExpenseTypesModel).order_by(ExpenseTypesModel.name)
		return [expense_type_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, expense_type_id: int) -> None:
		"""Delete one expense type row by identifier."""

		self._session.delete(self._require_model(expense_type_id))

	def _require_model(self, expense_type_id: int | None) -> ExpenseTypesModel:
		"""Resolve one expense type model or fail fast when the identifier is invalid."""

		if expense_type_id is None:
			raise ValueError("Expense type id is required for this operation.")
		model = self._session.get(ExpenseTypesModel, expense_type_id)
		if model is None:
			raise ValueError(f"Expense type with id {expense_type_id} was not found.")
		return model


class SqlAlchemyIncomeTypeRepository(IncomeTypeRepository):
	"""SQLAlchemy repository for income type catalog rows."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, income_type: IncomeType) -> IncomeType:
		"""Insert a new income type row and return the persisted model."""

		model = merge_income_type_into_model(income_type)
		self._session.add(model)
		self._session.flush()
		return income_type_to_entity(model)

	def update(self, income_type: IncomeType) -> IncomeType:
		"""Persist scalar field changes for an existing income type row."""

		model = self._require_model(income_type.id)
		merge_income_type_into_model(income_type, model)
		self._session.flush()
		return income_type_to_entity(model)

	def get_by_id(self, income_type_id: int) -> IncomeType | None:
		"""Load one income type row by identifier."""

		stmt = select(IncomeTypesModel).where(IncomeTypesModel.id == income_type_id)
		model = self._session.scalar(stmt)
		return income_type_to_entity(model) if model is not None else None

	def get_by_name(self, name: str) -> IncomeType | None:
		"""Load one income type row by its unique name."""

		stmt = select(IncomeTypesModel).where(IncomeTypesModel.name == name)
		model = self._session.scalar(stmt)
		return income_type_to_entity(model) if model is not None else None

	def list(self) -> Sequence[IncomeType]:
		"""Load all income type rows ordered by name."""

		stmt = select(IncomeTypesModel).order_by(IncomeTypesModel.name)
		return [income_type_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, income_type_id: int) -> None:
		"""Delete one income type row by identifier."""

		self._session.delete(self._require_model(income_type_id))

	def _require_model(self, income_type_id: int | None) -> IncomeTypesModel:
		"""Resolve one income type model or fail fast when the identifier is invalid."""

		if income_type_id is None:
			raise ValueError("Income type id is required for this operation.")
		model = self._session.get(IncomeTypesModel, income_type_id)
		if model is None:
			raise ValueError(f"Income type with id {income_type_id} was not found.")
		return model


class SqlAlchemyTaxTypeRepository(TaxTypeRepository):
	"""SQLAlchemy repository for tax type catalog rows."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, tax_type: TaxType) -> TaxType:
		"""Insert a new tax type row and return the persisted model."""

		model = merge_tax_type_into_model(tax_type)
		self._session.add(model)
		self._session.flush()
		return tax_type_to_entity(model)

	def update(self, tax_type: TaxType) -> TaxType:
		"""Persist scalar field changes for an existing tax type row."""

		model = self._require_model(tax_type.id)
		merge_tax_type_into_model(tax_type, model)
		self._session.flush()
		return tax_type_to_entity(model)

	def get_by_id(self, tax_type_id: int) -> TaxType | None:
		"""Load one tax type row by identifier."""

		stmt = select(TaxTypesModel).where(TaxTypesModel.id == tax_type_id)
		model = self._session.scalar(stmt)
		return tax_type_to_entity(model) if model is not None else None

	def get_by_name(self, name: str) -> TaxType | None:
		"""Load one tax type row by its unique name."""

		stmt = select(TaxTypesModel).where(TaxTypesModel.name == name)
		model = self._session.scalar(stmt)
		return tax_type_to_entity(model) if model is not None else None

	def list(self) -> Sequence[TaxType]:
		"""Load all tax type rows ordered by name."""

		stmt = select(TaxTypesModel).order_by(TaxTypesModel.name)
		return [tax_type_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, tax_type_id: int) -> None:
		"""Delete one tax type row by identifier."""

		self._session.delete(self._require_model(tax_type_id))

	def _require_model(self, tax_type_id: int | None) -> TaxTypesModel:
		"""Resolve one tax type model or fail fast when the identifier is invalid."""

		if tax_type_id is None:
			raise ValueError("Tax type id is required for this operation.")
		model = self._session.get(TaxTypesModel, tax_type_id)
		if model is None:
			raise ValueError(f"Tax type with id {tax_type_id} was not found.")
		return model


class SqlAlchemyPaymentRepository(PaymentRepository):
	"""SQLAlchemy repository for payment transactions."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, payment: Payment) -> Payment:
		"""Insert a new payment row and return the persisted model."""

		model = merge_payment_into_model(payment)
		self._session.add(model)
		self._session.flush()
		return payment_to_entity(model)

	def update(self, payment: Payment) -> Payment:
		"""Persist scalar field changes for an existing payment row."""

		model = self._require_payment_model(payment.id)
		merge_payment_into_model(payment, model)
		self._session.flush()
		return payment_to_entity(model)

	def get_by_id(self, payment_id: int) -> Payment | None:
		"""Load one payment transaction by identifier."""

		stmt = (
			select(PaymentsModel)
			.options(*_payment_load_options())
			.where(PaymentsModel.id == payment_id)
		)
		model = self._session.scalar(stmt)
		return payment_to_entity(model) if model is not None else None

	def list_by_asset(self, asset_id: int) -> Sequence[Payment]:
		"""Load payments linked to one asset ordered by registration date."""

		stmt = (
			select(PaymentsModel)
			.options(*_payment_load_options())
			.where(PaymentsModel.asset_id == asset_id)
			.order_by(PaymentsModel.registered_at.desc())
		)
		return [payment_to_entity(model) for model in self._session.scalars(stmt).all()]

	def add_attachment(self, attachment: PaymentAttachment) -> PaymentAttachment:
		"""Attach one evidence metadata row to a payment transaction."""

		model = merge_payment_attachment_into_model(attachment)
		self._require_payment_model(model.payment_id)
		self._session.add(model)
		self._session.flush()
		return payment_attachment_to_entity(model)

	def remove_attachment(self, attachment_id: int) -> None:
		"""Delete one payment attachment metadata row by identifier."""

		attachment = self._session.get(PaymentAttachmentModel, attachment_id)
		if attachment is not None:
			self._session.delete(attachment)
			self._session.flush()

	def delete(self, payment_id: int) -> None:
		"""Delete one payment transaction by identifier."""

		self._session.delete(self._require_payment_model(payment_id))

	def _require_payment_model(self, payment_id: int | None) -> PaymentsModel:
		"""Resolve one payment model or fail fast when the identifier is invalid."""

		if payment_id is None:
			raise ValueError("Payment id is required for this operation.")
		model = self._session.get(PaymentsModel, payment_id)
		if model is None:
			raise ValueError(f"Payment with id {payment_id} was not found.")
		return model


class SqlAlchemyExpenseRepository(ExpenseRepository):
	"""SQLAlchemy repository for expense transactions."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, expense: Expense) -> Expense:
		"""Insert a new expense row and return the persisted model."""

		model = merge_expense_into_model(expense)
		self._session.add(model)
		self._session.flush()
		return expense_to_entity(model)

	def update(self, expense: Expense) -> Expense:
		"""Persist scalar field changes for an existing expense row."""

		model = self._require_model(expense.id)
		merge_expense_into_model(expense, model)
		self._session.flush()
		return expense_to_entity(model)

	def get_by_id(self, expense_id: int) -> Expense | None:
		"""Load one expense transaction by identifier."""

		stmt = (
			select(ExpenseModel)
			.options(selectinload(ExpenseModel.expense_type), selectinload(ExpenseModel.payment))
			.where(ExpenseModel.id == expense_id)
		)
		model = self._session.scalar(stmt)
		return expense_to_entity(model) if model is not None else None

	def list_by_asset(self, asset_id: int) -> Sequence[Expense]:
		"""Load expenses linked to one asset ordered by registration date."""

		stmt = (
			select(ExpenseModel)
			.options(selectinload(ExpenseModel.expense_type), selectinload(ExpenseModel.payment))
			.where(ExpenseModel.asset_id == asset_id)
			.order_by(ExpenseModel.registered_at.desc())
		)
		return [expense_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, expense_id: int) -> None:
		"""Delete one expense transaction by identifier."""

		self._session.delete(self._require_model(expense_id))

	def _require_model(self, expense_id: int | None) -> ExpenseModel:
		"""Resolve one expense model or fail fast when the identifier is invalid."""

		if expense_id is None:
			raise ValueError("Expense id is required for this operation.")
		model = self._session.get(ExpenseModel, expense_id)
		if model is None:
			raise ValueError(f"Expense with id {expense_id} was not found.")
		return model


class SqlAlchemyIncomeRepository(IncomeRepository):
	"""SQLAlchemy repository for income transactions."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, income: Income) -> Income:
		"""Insert a new income row and return the persisted model."""

		model = merge_income_into_model(income)
		self._session.add(model)
		self._session.flush()
		return income_to_entity(model)

	def update(self, income: Income) -> Income:
		"""Persist scalar field changes for an existing income row."""

		model = self._require_model(income.id)
		merge_income_into_model(income, model)
		self._session.flush()
		return income_to_entity(model)

	def get_by_id(self, income_id: int) -> Income | None:
		"""Load one income transaction by identifier."""

		stmt = (
			select(IncomeModel)
			.options(selectinload(IncomeModel.income_type), selectinload(IncomeModel.payment))
			.where(IncomeModel.id == income_id)
		)
		model = self._session.scalar(stmt)
		return income_to_entity(model) if model is not None else None

	def list_by_asset(self, asset_id: int) -> Sequence[Income]:
		"""Load incomes linked to one asset ordered by registration date."""

		stmt = (
			select(IncomeModel)
			.options(selectinload(IncomeModel.income_type), selectinload(IncomeModel.payment))
			.where(IncomeModel.asset_id == asset_id)
			.order_by(IncomeModel.registered_at.desc())
		)
		return [income_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, income_id: int) -> None:
		"""Delete one income transaction by identifier."""

		self._session.delete(self._require_model(income_id))

	def _require_model(self, income_id: int | None) -> IncomeModel:
		"""Resolve one income model or fail fast when the identifier is invalid."""

		if income_id is None:
			raise ValueError("Income id is required for this operation.")
		model = self._session.get(IncomeModel, income_id)
		if model is None:
			raise ValueError(f"Income with id {income_id} was not found.")
		return model


class SqlAlchemyInvoiceRepository(InvoiceRepository):
	"""SQLAlchemy repository for invoice aggregates."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, invoice: Invoice) -> Invoice:
		"""Insert a new invoice row and return the persisted model."""

		model = merge_invoice_into_model(invoice)
		self._session.add(model)
		self._session.flush()
		return invoice_to_entity(model)

	def update(self, invoice: Invoice) -> Invoice:
		"""Persist scalar field changes for an existing invoice row."""

		model = self._require_invoice_model(invoice.id)
		merge_invoice_into_model(invoice, model)
		self._session.flush()
		return invoice_to_entity(model)

	def get_by_id(self, invoice_id: int) -> Invoice | None:
		"""Load one invoice aggregate by identifier."""

		stmt = (
			select(InvoiceModel)
			.options(*_invoice_load_options())
			.where(InvoiceModel.id == invoice_id)
		)
		model = self._session.scalar(stmt)
		return invoice_to_entity(model) if model is not None else None

	def list_by_asset(self, asset_id: int) -> Sequence[Invoice]:
		"""Load invoices linked to one asset ordered by issue date."""

		stmt = (
			select(InvoiceModel)
			.options(*_invoice_load_options())
			.where(InvoiceModel.asset_id == asset_id)
			.order_by(InvoiceModel.issued_at.desc())
		)
		return [invoice_to_entity(model) for model in self._session.scalars(stmt).all()]

	def add_line(self, line: InvoiceLine) -> InvoiceLine:
		"""Attach one line row to an invoice."""

		model = merge_invoice_line_into_model(line)
		self._require_invoice_model(model.invoice_id)
		self._session.add(model)
		self._session.flush()
		return invoice_line_to_entity(model)

	def remove_line(self, line_id: int) -> None:
		"""Delete one invoice line row by identifier."""

		line = self._session.get(InvoiceLineModel, line_id)
		if line is not None:
			self._session.delete(line)
			self._session.flush()

	def add_document(self, document: InvoiceDocument) -> InvoiceDocument:
		"""Attach one document metadata row to an invoice."""

		model = merge_invoice_document_into_model(document)
		self._require_invoice_model(model.invoice_id)
		self._session.add(model)
		self._session.flush()
		return invoice_document_to_entity(model)

	def remove_document(self, document_id: int) -> None:
		"""Delete one invoice document metadata row by identifier."""

		document = self._session.get(InvoiceDocumentModel, document_id)
		if document is not None:
			self._session.delete(document)
			self._session.flush()

	def delete(self, invoice_id: int) -> None:
		"""Delete one invoice aggregate by identifier."""

		self._session.delete(self._require_invoice_model(invoice_id))

	def _require_invoice_model(self, invoice_id: int | None) -> InvoiceModel:
		"""Resolve one invoice model or fail fast when the identifier is invalid."""

		if invoice_id is None:
			raise ValueError("Invoice id is required for this operation.")
		model = self._session.get(InvoiceModel, invoice_id)
		if model is None:
			raise ValueError(f"Invoice with id {invoice_id} was not found.")
		return model


def _payment_load_options() -> tuple:
	"""Define eager-load paths required to load one payment aggregate."""

	return (
		selectinload(PaymentsModel.expenses),
		selectinload(PaymentsModel.incomes),
		selectinload(PaymentsModel.attachments),
	)


def _invoice_load_options() -> tuple:
	"""Define eager-load paths required to load one invoice aggregate."""

	return (
		selectinload(InvoiceModel.lines),
		selectinload(InvoiceModel.documents),
	)
