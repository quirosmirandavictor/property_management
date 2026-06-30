from __future__ import annotations

from sqlalchemy.orm import Session


class SqlAlchemyAssetRepository:
	"""Template repository for the Assets module.

	This module should contain persistence operations for the Asset aggregate.
	Add query methods here when they answer business use cases of the Assets module.
	Keep transaction boundaries outside the repository and let a unit of work commit.
	"""

	def __init__(self, session: Session) -> None:
		"""Store the SQLAlchemy session received from the application layer."""

		self._session = session

	def add(self, asset: object) -> object:
		"""Create a new asset aggregate.

		Replace `object` with the domain entity once the Assets domain layer is defined.
		"""

		raise NotImplementedError

	def update(self, asset: object) -> object:
		"""Persist scalar changes for an existing asset aggregate."""

		raise NotImplementedError

	def get_by_id(self, asset_id: int) -> object | None:
		"""Return one asset aggregate by identifier."""

		raise NotImplementedError

	def list(self) -> list[object]:
		"""Return asset aggregates using the ordering and filters required by the module."""

		raise NotImplementedError

	def delete(self, asset_id: int) -> None:
		"""Delete one asset aggregate by identifier."""

		raise NotImplementedError
