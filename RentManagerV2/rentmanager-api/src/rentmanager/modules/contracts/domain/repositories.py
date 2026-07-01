from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from rentmanager.modules.contracts.domain.entities import Contract
from rentmanager.modules.contracts.domain.entities import ContractDocument


class ContractRepository(ABC):
	"""Contract for persisting and retrieving contract aggregates."""

	@abstractmethod
	def add(self, contract: Contract) -> Contract:
		"""Persist a new contract aggregate and return its current state."""

	@abstractmethod
	def update(self, contract: Contract) -> Contract:
		"""Persist scalar changes for an existing contract aggregate."""

	@abstractmethod
	def get_by_id(self, contract_id: int) -> Contract | None:
		"""Return one contract aggregate by identifier."""

	@abstractmethod
	def get_by_code(self, contract_code: str) -> Contract | None:
		"""Return one contract aggregate by business code."""

	@abstractmethod
	def list_by_asset(self, asset_id: int) -> Sequence[Contract]:
		"""Return contracts linked to one asset."""

	@abstractmethod
	def add_tenant(self, contract_id: int, user_id: int, role_in_contract: str) -> None:
		"""Attach one tenant to one contract if the pair does not already exist."""

	@abstractmethod
	def remove_tenant(self, contract_id: int, user_id: int) -> None:
		"""Detach one tenant from one contract if the pair exists."""

	@abstractmethod
	def add_document(self, document: ContractDocument) -> ContractDocument:
		"""Attach one document metadata record to a contract."""

	@abstractmethod
	def remove_document(self, document_id: int) -> None:
		"""Delete one contract document metadata record by identifier."""

	@abstractmethod
	def delete(self, contract_id: int) -> None:
		"""Delete one contract aggregate by identifier."""
