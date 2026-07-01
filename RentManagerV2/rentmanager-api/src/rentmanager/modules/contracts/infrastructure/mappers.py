from __future__ import annotations

from rentmanager.modules.contracts.domain.entities import Contract
from rentmanager.modules.contracts.domain.entities import ContractDocument
from rentmanager.modules.contracts.domain.entities import TenantContract
from rentmanager.modules.contracts.infrastructure.models import ContractDocumentModel
from rentmanager.modules.contracts.infrastructure.models import ContractModel
from rentmanager.modules.contracts.infrastructure.models import TenantContractModel


def tenant_contract_to_entity(model: TenantContractModel) -> TenantContract:
	"""Translate one ORM tenant-contract row into a domain entity."""

	return TenantContract(
		id=model.id,
		contract_id=model.contract_id,
		user_id=model.user_id,
		role_in_contract=model.role_in_contract,
	)


def contract_document_to_entity(model: ContractDocumentModel) -> ContractDocument:
	"""Translate one ORM contract document row into a domain entity."""

	return ContractDocument(
		id=model.id,
		contract_id=model.contract_id,
		category=model.category,
		original_filename=model.original_filename,
		content_type=model.content_type,
		size_bytes=model.size_bytes,
		blob_container=model.blob_container,
		blob_key=model.blob_key,
	)


def contract_to_entity(model: ContractModel) -> Contract:
	"""Translate one ORM contract row into a domain aggregate."""

	return Contract(
		id=model.id,
		contract_code=model.contract_code,
		asset_id=model.asset_id,
		start_date=model.start_date,
		end_date=model.end_date,
		rent_amount=model.rent_amount,
		deposit_amount=model.deposit_amount,
		status=model.status,
		created_at=model.created_at,
		updated_at=model.updated_at,
		tenant_contracts=[tenant_contract_to_entity(item) for item in model.tenant_contracts],
		documents=[contract_document_to_entity(item) for item in model.documents],
	)


def merge_contract_into_model(entity: Contract, model: ContractModel | None = None) -> ContractModel:
	"""Copy scalar domain fields into an ORM contract instance."""

	model = model or ContractModel()
	model.contract_code = entity.contract_code
	model.asset_id = entity.asset_id
	model.start_date = entity.start_date
	model.end_date = entity.end_date
	model.rent_amount = entity.rent_amount
	model.deposit_amount = entity.deposit_amount
	model.status = entity.status
	return model


def merge_document_into_model(
	entity: ContractDocument,
	model: ContractDocumentModel | None = None,
) -> ContractDocumentModel:
	"""Copy scalar domain fields into an ORM contract-document instance."""

	model = model or ContractDocumentModel()
	model.contract_id = entity.contract_id
	model.category = entity.category
	model.original_filename = entity.original_filename
	model.content_type = entity.content_type
	model.size_bytes = entity.size_bytes
	model.blob_container = entity.blob_container
	model.blob_key = entity.blob_key
	return model
