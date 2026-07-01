from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from rentmanager.modules.assets.domain.entities import Asset


class AssetRepository(ABC):
	"""Contract for persisting and retrieving asset aggregates."""

	@abstractmethod
	def add(self, asset: Asset) -> Asset:
		"""Persist a new asset aggregate and return its current state."""

	@abstractmethod
	def update(self, asset: Asset) -> Asset:
		"""Persist scalar changes for an existing asset aggregate."""

	@abstractmethod
	def get_by_id(self, asset_id: int) -> Asset | None:
		"""Return one asset aggregate by identifier."""

	@abstractmethod
	def get_by_code(self, asset_code: str) -> Asset | None:
		"""Return one asset aggregate by business code."""

	@abstractmethod
	def list(self, *, status: str | None = None) -> Sequence[Asset]:
		"""Return asset aggregates with an optional status filter."""

	@abstractmethod
	def delete(self, asset_id: int) -> None:
		"""Delete one asset aggregate by identifier."""
