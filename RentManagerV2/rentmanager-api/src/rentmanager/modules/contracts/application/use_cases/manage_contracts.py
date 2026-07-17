from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from rentmanager.modules.assets.domain.repositories import AssetRepository
from rentmanager.modules.contracts.application.dtos import (
	ContractDocumentOutput,
	ContractOutput,
	CreateContractDocumentInput,
	CreateContractInput,
	TenantContractOutput,
)
from rentmanager.modules.contracts.domain.entities import Contract, ContractDocument
from rentmanager.modules.contracts.domain.exceptions import (
	ContractCodeAlreadyExistsError,
	ContractNotFoundError,
	ContractTenantAlreadyAssignedError,
	ContractTenantNotFoundError,
	InvalidContractStateError,
)
from rentmanager.modules.contracts.domain.repositories import ContractRepository
from rentmanager.modules.iam.domain.repositories import UserRepository

_ALLOWED_CONTRACT_STATUSES = {"draft", "active", "terminated", "expired"}
_ALLOWED_TENANT_ROLES = {"tenant", "co-tenant", "guarantor"}


class ManageContractsUseCase:
	"""Orchestrate contract CRUD and aggregate child operations."""

	def __init__(
		self,
		contract_repository: ContractRepository,
		asset_repository: AssetRepository,
		user_repository: UserRepository,
	) -> None:
		self._contract_repository = contract_repository
		self._asset_repository = asset_repository
		self._user_repository = user_repository

	def create(self, payload: CreateContractInput) -> ContractOutput:
		if self._contract_repository.get_by_code(payload.contract_code) is not None:
			raise ContractCodeAlreadyExistsError("Contract code is already registered.")
		if self._asset_repository.get_by_id(payload.asset_id) is None:
			raise InvalidContractStateError("Asset does not exist for this contract.")

		contract = Contract(
			id=None,
			contract_code=payload.contract_code,
			asset_id=payload.asset_id,
			start_date=payload.start_date,
			end_date=payload.end_date,
			rent_amount=payload.rent_amount,
			deposit_amount=payload.deposit_amount,
			status=payload.status,
		)
		self._validate_contract(contract)

		persisted = self._contract_repository.add(contract)
		return self._to_output(persisted)

	def get(self, contract_id: int) -> ContractOutput:
		contract = self._contract_repository.get_by_id(contract_id)
		if contract is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		return self._to_output(contract)

	def list(
		self,
		*,
		asset_id: int | None = None,
		status: str | None = None,
	) -> Sequence[ContractOutput]:
		if status is not None and status not in _ALLOWED_CONTRACT_STATUSES:
			raise InvalidContractStateError("Contract status filter is invalid.")
		contracts = self._contract_repository.list(asset_id=asset_id, status=status)
		return [self._to_output(contract) for contract in contracts]

	def update(self, contract_id: int, updates: Mapping[str, Any]) -> ContractOutput:
		current = self._contract_repository.get_by_id(contract_id)
		if current is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")

		if "contract_code" in updates:
			contract_code = updates["contract_code"]
			if isinstance(contract_code, str) and contract_code != current.contract_code:
				by_code = self._contract_repository.get_by_code(contract_code)
				if by_code is not None and by_code.id != current.id:
					raise ContractCodeAlreadyExistsError("Contract code is already registered.")

		if "asset_id" in updates:
			asset_id = updates["asset_id"]
			if isinstance(asset_id, int) and self._asset_repository.get_by_id(asset_id) is None:
				raise InvalidContractStateError("Asset does not exist for this contract.")

		for field_name, field_value in updates.items():
			if hasattr(current, field_name):
				setattr(current, field_name, field_value)

		self._validate_contract(current)
		updated = self._contract_repository.update(current)
		return self._to_output(updated)

	def delete(self, contract_id: int) -> None:
		if self._contract_repository.get_by_id(contract_id) is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		self._contract_repository.delete(contract_id)

	def add_tenant(self, contract_id: int, user_id: int, role_in_contract: str) -> ContractOutput:
		contract = self._contract_repository.get_by_id(contract_id)
		if contract is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		if self._user_repository.get_by_id(user_id) is None:
			raise InvalidContractStateError("Tenant user does not exist.")
		if role_in_contract not in _ALLOWED_TENANT_ROLES:
			raise InvalidContractStateError(
				"Tenant role must be one of: tenant, co-tenant, guarantor."
			)
		for assignment in contract.tenant_contracts:
			if assignment.user_id == user_id:
				raise ContractTenantAlreadyAssignedError(
					"Tenant is already assigned to this contract."
				)

		self._contract_repository.add_tenant(
			contract_id=contract_id,
			user_id=user_id,
			role_in_contract=role_in_contract,
		)
		updated = self._contract_repository.get_by_id(contract_id)
		if updated is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		return self._to_output(updated)

	def remove_tenant(self, contract_id: int, user_id: int) -> ContractOutput:
		contract = self._contract_repository.get_by_id(contract_id)
		if contract is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		if all(item.user_id != user_id for item in contract.tenant_contracts):
			raise ContractTenantNotFoundError("Tenant is not assigned to this contract.")

		self._contract_repository.remove_tenant(contract_id=contract_id, user_id=user_id)
		updated = self._contract_repository.get_by_id(contract_id)
		if updated is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		return self._to_output(updated)

	def add_document(self, payload: CreateContractDocumentInput) -> ContractOutput:
		contract = self._contract_repository.get_by_id(payload.contract_id)
		if contract is None:
			raise ContractNotFoundError(f"Contract with id {payload.contract_id} was not found.")
		if payload.size_bytes <= 0:
			raise InvalidContractStateError("Document size must be greater than zero bytes.")

		document = ContractDocument(
			id=None,
			contract_id=payload.contract_id,
			category=payload.category,
			original_filename=payload.original_filename,
			content_type=payload.content_type,
			size_bytes=payload.size_bytes,
			blob_container=payload.blob_container,
			blob_key=payload.blob_key,
		)
		self._contract_repository.add_document(document)

		updated = self._contract_repository.get_by_id(payload.contract_id)
		if updated is None:
			raise ContractNotFoundError(f"Contract with id {payload.contract_id} was not found.")
		return self._to_output(updated)

	def remove_document(self, contract_id: int, document_id: int) -> ContractOutput:
		contract = self._contract_repository.get_by_id(contract_id)
		if contract is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		if all(document.id != document_id for document in contract.documents):
			raise InvalidContractStateError("Contract document was not found.")

		self._contract_repository.remove_document(document_id)
		updated = self._contract_repository.get_by_id(contract_id)
		if updated is None:
			raise ContractNotFoundError(f"Contract with id {contract_id} was not found.")
		return self._to_output(updated)

	def _validate_contract(self, contract: Contract) -> None:
		if contract.status not in _ALLOWED_CONTRACT_STATUSES:
			raise InvalidContractStateError(
				"Contract status must be one of: draft, active, terminated, expired."
			)
		if contract.end_date <= contract.start_date:
			raise InvalidContractStateError("Contract end date must be later than start date.")
		if contract.rent_amount < Decimal("0"):
			raise InvalidContractStateError("Rent amount cannot be negative.")
		if contract.deposit_amount < Decimal("0"):
			raise InvalidContractStateError("Deposit amount cannot be negative.")

	def _to_output(self, contract: Contract) -> ContractOutput:
		if contract.id is None:
			raise InvalidContractStateError("Contract identity is invalid.")
		return ContractOutput(
			id=contract.id,
			contract_code=contract.contract_code,
			asset_id=contract.asset_id,
			start_date=contract.start_date,
			end_date=contract.end_date,
			rent_amount=contract.rent_amount,
			deposit_amount=contract.deposit_amount,
			status=contract.status,
			created_at=contract.created_at,
			updated_at=contract.updated_at,
			tenant_contracts=[
				TenantContractOutput(
					id=item.id,
					contract_id=item.contract_id,
					user_id=item.user_id,
					role_in_contract=item.role_in_contract,
				)
				for item in contract.tenant_contracts
			],
			documents=[
				ContractDocumentOutput(
					id=item.id,
					contract_id=item.contract_id,
					category=item.category,
					original_filename=item.original_filename,
					content_type=item.content_type,
					size_bytes=item.size_bytes,
					blob_container=item.blob_container,
					blob_key=item.blob_key,
					uploaded_at=item.uploaded_at,
				)
				for item in contract.documents
			],
		)
