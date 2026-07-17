from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from rentmanager.modules.contracts.domain.entities import Contract, ContractDocument
from rentmanager.modules.contracts.domain.repositories import ContractRepository
from rentmanager.modules.contracts.infrastructure.mappers import (
	contract_document_to_entity,
	contract_to_entity,
	merge_contract_into_model,
	merge_document_into_model,
)
from rentmanager.modules.contracts.infrastructure.models import (
	ContractDocumentModel,
	ContractModel,
	TenantContractModel,
)
from rentmanager.modules.iam.infrastructure.models import UserModel


class SqlAlchemyContractRepository(ContractRepository):
	"""SQLAlchemy repository for the Contract aggregate."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, contract: Contract) -> Contract:
		"""Insert a new contract row and return the persisted aggregate."""

		model = merge_contract_into_model(contract)
		self._session.add(model)
		self._session.flush()
		return contract_to_entity(model)

	def update(self, contract: Contract) -> Contract:
		"""Persist scalar field changes for an existing contract aggregate."""

		model = self._require_contract_model(contract.id)
		merge_contract_into_model(contract, model)
		self._session.flush()
		return contract_to_entity(model)

	def get_by_id(self, contract_id: int) -> Contract | None:
		"""Load one contract aggregate by identifier."""

		stmt = (
			select(ContractModel)
			.options(*_contract_load_options())
			.where(ContractModel.id == contract_id)
		)
		model = self._session.scalar(stmt)
		return contract_to_entity(model) if model is not None else None

	def get_by_code(self, contract_code: str) -> Contract | None:
		"""Load one contract aggregate by contract code."""

		stmt = (
			select(ContractModel)
			.options(*_contract_load_options())
			.where(ContractModel.contract_code == contract_code)
		)
		model = self._session.scalar(stmt)
		return contract_to_entity(model) if model is not None else None

	def list(self, *, asset_id: int | None = None, status: str | None = None) -> Sequence[Contract]:
		"""Load contracts filtered by optional asset and status criteria."""

		stmt = select(ContractModel).options(*_contract_load_options())
		if asset_id is not None:
			stmt = stmt.where(ContractModel.asset_id == asset_id)
		if status is not None:
			stmt = stmt.where(ContractModel.status == status)
		stmt = stmt.order_by(ContractModel.start_date.desc())
		return [contract_to_entity(model) for model in self._session.scalars(stmt).all()]

	def list_by_asset(self, asset_id: int) -> Sequence[Contract]:
		"""Load contracts that belong to one asset."""
		return self.list(asset_id=asset_id)

	def add_tenant(self, contract_id: int, user_id: int, role_in_contract: str) -> None:
		"""Attach one tenant to one contract if the pair does not already exist."""

		contract = self._require_contract_model(contract_id)
		self._require_user_model(user_id)
		for assignment in contract.tenant_contracts:
			if assignment.user_id == user_id:
				return

		tenant_contract = TenantContractModel(
			contract_id=contract_id,
			user_id=user_id,
			role_in_contract=role_in_contract,
		)
		self._session.add(tenant_contract)
		self._session.flush()

	def remove_tenant(self, contract_id: int, user_id: int) -> None:
		"""Detach one tenant from one contract if the pair exists."""

		stmt = select(TenantContractModel).where(
			TenantContractModel.contract_id == contract_id,
			TenantContractModel.user_id == user_id,
		)
		assignment = self._session.scalar(stmt)
		if assignment is not None:
			self._session.delete(assignment)
			self._session.flush()

	def add_document(self, document: ContractDocument) -> ContractDocument:
		"""Attach one document metadata record to a contract."""

		model = merge_document_into_model(document)
		self._require_contract_model(model.contract_id)
		self._session.add(model)
		self._session.flush()
		return contract_document_to_entity(model)

	def remove_document(self, document_id: int) -> None:
		"""Delete one contract document metadata row by identifier."""

		document = self._session.get(ContractDocumentModel, document_id)
		if document is not None:
			self._session.delete(document)
			self._session.flush()

	def delete(self, contract_id: int) -> None:
		"""Delete one contract aggregate by identifier."""

		self._session.delete(self._require_contract_model(contract_id))

	def _require_contract_model(self, contract_id: int | None) -> ContractModel:
		"""Resolve one contract model or fail fast when the identifier is invalid."""

		if contract_id is None:
			raise ValueError("Contract id is required for this operation.")
		model = self._session.get(ContractModel, contract_id)
		if model is None:
			raise ValueError(f"Contract with id {contract_id} was not found.")
		return model

	def _require_user_model(self, user_id: int | None) -> UserModel:
		"""Resolve one IAM user model or fail fast when the identifier is invalid."""

		if user_id is None:
			raise ValueError("User id is required for this operation.")
		model = self._session.get(UserModel, user_id)
		if model is None:
			raise ValueError(f"User with id {user_id} was not found.")
		return model


def _contract_load_options() -> tuple:
	"""Define eager-load paths required to load a full contract aggregate."""

	return (
		selectinload(ContractModel.tenant_contracts).selectinload(TenantContractModel.user),
		selectinload(ContractModel.documents),
	)
