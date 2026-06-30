from __future__ import annotations

from sqlalchemy.orm import Session


class SqlAlchemyFinanceRepository:
	"""Template repository for the Finance module.

	The Finance module usually benefits from several repositories instead of one,
	for example payments, expenses, incomes, and invoices. This placeholder keeps
	the shape visible until the finance domain contracts are defined.
	"""

	def __init__(self, session: Session) -> None:
		"""Store the SQLAlchemy session received from the application layer."""

		self._session = session

	def add(self, aggregate: object) -> object:
		"""Create a new finance aggregate or transactional record."""

		raise NotImplementedError

	def update(self, aggregate: object) -> object:
		"""Persist scalar changes for an existing finance aggregate."""

		raise NotImplementedError

	def get_by_id(self, aggregate_id: int) -> object | None:
		"""Return one finance aggregate by identifier."""

		raise NotImplementedError

	def list_by_asset(self, asset_id: int) -> list[object]:
		"""Return finance records associated with one asset."""

		raise NotImplementedError

	def delete(self, aggregate_id: int) -> None:
		"""Delete one finance aggregate by identifier."""

		raise NotImplementedError
