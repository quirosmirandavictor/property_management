from __future__ import annotations

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


def expense_type_to_entity(model: ExpenseTypesModel) -> ExpenseType:
	"""Translate one ORM expense-type row into a domain entity."""

	return ExpenseType(id=model.id, name=model.name, description=model.description)


def income_type_to_entity(model: IncomeTypesModel) -> IncomeType:
	"""Translate one ORM income-type row into a domain entity."""

	return IncomeType(id=model.id, name=model.name, description=model.description)


def tax_type_to_entity(model: TaxTypesModel) -> TaxType:
	"""Translate one ORM tax-type row into a domain entity."""

	return TaxType(
		id=model.id,
		name=model.name,
		description=model.description,
		tax_percentage=model.tax_percentage,
	)


def payment_attachment_to_entity(model: PaymentAttachmentModel) -> PaymentAttachment:
	"""Translate one ORM payment-attachment row into a domain entity."""

	return PaymentAttachment(
		id=model.id,
		payment_id=model.payment_id,
		original_filename=model.original_filename,
		content_type=model.content_type,
		size_bytes=model.size_bytes,
		blob_container=model.blob_container,
		blob_key=model.blob_key,
		uploaded_at=model.uploaded_at,
	)


def payment_to_entity(model: PaymentsModel) -> Payment:
	"""Translate one ORM payment row into a domain aggregate."""

	return Payment(
		id=model.id,
		asset_id=model.asset_id,
		registered_at=model.registered_at,
		bank_reference=model.bank_reference,
		amount=model.amount,
		description=model.description,
		status=model.status,
		created_at=model.created_at,
		updated_at=model.updated_at,
		attachments=[payment_attachment_to_entity(item) for item in model.attachments],
	)


def expense_to_entity(model: ExpenseModel) -> Expense:
	"""Translate one ORM expense row into a domain entity."""

	return Expense(
		id=model.id,
		asset_id=model.asset_id,
		expense_type_id=model.expense_type_id,
		payment_id=model.payment_id,
		amount=model.amount,
		registered_at=model.registered_at,
		description=model.description,
		deductible=model.deductible,
		created_at=model.created_at,
		updated_at=model.updated_at,
	)


def income_to_entity(model: IncomeModel) -> Income:
	"""Translate one ORM income row into a domain entity."""

	return Income(
		id=model.id,
		asset_id=model.asset_id,
		income_type_id=model.income_type_id,
		payment_id=model.payment_id,
		amount=model.amount,
		registered_at=model.registered_at,
		description=model.description,
		created_at=model.created_at,
		updated_at=model.updated_at,
	)


def invoice_line_to_entity(model: InvoiceLineModel) -> InvoiceLine:
	"""Translate one ORM invoice-line row into a domain entity."""

	return InvoiceLine(
		id=model.id,
		invoice_id=model.invoice_id,
		expense_id=model.expense_id,
		income_id=model.income_id,
		line_type=model.line_type,
		amount=model.amount,
		created_at=model.created_at,
		updated_at=model.updated_at,
	)


def invoice_document_to_entity(model: InvoiceDocumentModel) -> InvoiceDocument:
	"""Translate one ORM invoice-document row into a domain entity."""

	return InvoiceDocument(
		id=model.id,
		invoice_id=model.invoice_id,
		original_filename=model.original_filename,
		content_type=model.content_type,
		size_bytes=model.size_bytes,
		blob_container=model.blob_container,
		blob_key=model.blob_key,
		uploaded_at=model.uploaded_at,
	)


def invoice_to_entity(model: InvoiceModel) -> Invoice:
	"""Translate one ORM invoice row into a domain aggregate."""

	return Invoice(
		id=model.id,
		asset_id=model.asset_id,
		issued_at=model.issued_at,
		total_amount=model.total_amount,
		status=model.status,
		created_at=model.created_at,
		updated_at=model.updated_at,
		lines=[invoice_line_to_entity(item) for item in model.lines],
		documents=[invoice_document_to_entity(item) for item in model.documents],
	)


def merge_expense_type_into_model(
	entity: ExpenseType,
	model: ExpenseTypesModel | None = None,
) -> ExpenseTypesModel:
	"""Copy scalar domain fields into an ORM expense-type instance."""

	model = model or ExpenseTypesModel()
	model.name = entity.name
	model.description = entity.description
	return model


def merge_income_type_into_model(
	entity: IncomeType,
	model: IncomeTypesModel | None = None,
) -> IncomeTypesModel:
	"""Copy scalar domain fields into an ORM income-type instance."""

	model = model or IncomeTypesModel()
	model.name = entity.name
	model.description = entity.description
	return model


def merge_tax_type_into_model(entity: TaxType, model: TaxTypesModel | None = None) -> TaxTypesModel:
	"""Copy scalar domain fields into an ORM tax-type instance."""

	model = model or TaxTypesModel()
	model.name = entity.name
	model.description = entity.description
	model.tax_percentage = entity.tax_percentage
	return model


def merge_payment_into_model(entity: Payment, model: PaymentsModel | None = None) -> PaymentsModel:
	"""Copy scalar domain fields into an ORM payment instance."""

	model = model or PaymentsModel()
	model.asset_id = entity.asset_id
	model.registered_at = entity.registered_at
	model.bank_reference = entity.bank_reference
	model.amount = entity.amount
	model.description = entity.description
	model.status = entity.status
	return model


def merge_payment_attachment_into_model(
	entity: PaymentAttachment,
	model: PaymentAttachmentModel | None = None,
) -> PaymentAttachmentModel:
	"""Copy scalar domain fields into an ORM payment-attachment instance."""

	model = model or PaymentAttachmentModel()
	model.payment_id = entity.payment_id
	model.original_filename = entity.original_filename
	model.content_type = entity.content_type
	model.size_bytes = entity.size_bytes
	model.blob_container = entity.blob_container
	model.blob_key = entity.blob_key
	return model


def merge_expense_into_model(entity: Expense, model: ExpenseModel | None = None) -> ExpenseModel:
	"""Copy scalar domain fields into an ORM expense instance."""

	model = model or ExpenseModel()
	model.asset_id = entity.asset_id
	model.expense_type_id = entity.expense_type_id
	model.payment_id = entity.payment_id
	model.amount = entity.amount
	model.registered_at = entity.registered_at
	model.description = entity.description
	model.deductible = entity.deductible
	return model


def merge_income_into_model(entity: Income, model: IncomeModel | None = None) -> IncomeModel:
	"""Copy scalar domain fields into an ORM income instance."""

	model = model or IncomeModel()
	model.asset_id = entity.asset_id
	model.income_type_id = entity.income_type_id
	model.payment_id = entity.payment_id
	model.amount = entity.amount
	model.registered_at = entity.registered_at
	model.description = entity.description
	return model


def merge_invoice_into_model(entity: Invoice, model: InvoiceModel | None = None) -> InvoiceModel:
	"""Copy scalar domain fields into an ORM invoice instance."""

	model = model or InvoiceModel()
	model.asset_id = entity.asset_id
	model.issued_at = entity.issued_at
	model.total_amount = entity.total_amount
	model.status = entity.status
	return model


def merge_invoice_line_into_model(
	entity: InvoiceLine,
	model: InvoiceLineModel | None = None,
) -> InvoiceLineModel:
	"""Copy scalar domain fields into an ORM invoice-line instance."""

	model = model or InvoiceLineModel()
	model.invoice_id = entity.invoice_id
	model.expense_id = entity.expense_id
	model.income_id = entity.income_id
	model.line_type = entity.line_type
	model.amount = entity.amount
	return model


def merge_invoice_document_into_model(
	entity: InvoiceDocument,
	model: InvoiceDocumentModel | None = None,
) -> InvoiceDocumentModel:
	"""Copy scalar domain fields into an ORM invoice-document instance."""

	model = model or InvoiceDocumentModel()
	model.invoice_id = entity.invoice_id
	model.original_filename = entity.original_filename
	model.content_type = entity.content_type
	model.size_bytes = entity.size_bytes
	model.blob_container = entity.blob_container
	model.blob_key = entity.blob_key
	return model
