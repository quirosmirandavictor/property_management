from __future__ import annotations

from sqlalchemy.orm import Session


class SqlAlchemyContractRepository:
	"""Template repository for the Contracts module.

	This module should contain persistence operations for the Contract aggregate,
	including contract documents and tenant associations when those belong to the
	aggregate boundary.
	"""

	def __init__(self, session: Session) -> None:
		"""Store the SQLAlchemy session received from the application layer."""

		self._session = session

	def add(self, contract: object) -> object:
		"""Create a new contract aggregate."""

		raise NotImplementedError

	def update(self, contract: object) -> object:
		"""Persist scalar changes for an existing contract aggregate."""

		raise NotImplementedError

	def get_by_id(self, contract_id: int) -> object | None:
		"""Return one contract aggregate by identifier."""

		raise NotImplementedError

	def list_by_asset(self, asset_id: int) -> list[object]:
		"""Return contracts that belong to one asset."""

		raise NotImplementedError

	def delete(self, contract_id: int) -> None:
		"""Delete one contract aggregate by identifier."""

		raise NotImplementedError
