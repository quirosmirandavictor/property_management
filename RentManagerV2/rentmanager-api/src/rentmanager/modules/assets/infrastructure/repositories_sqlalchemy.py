from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from rentmanager.modules.assets.domain.entities import Asset
from rentmanager.modules.assets.domain.repositories import AssetRepository
from rentmanager.modules.assets.infrastructure.mappers import asset_to_entity
from rentmanager.modules.assets.infrastructure.mappers import merge_asset_into_model
from rentmanager.modules.assets.infrastructure.models import AssetModel


class SqlAlchemyAssetRepository(AssetRepository):
	"""SQLAlchemy repository for the Asset aggregate."""

	def __init__(self, session: Session) -> None:
		"""Store the active SQLAlchemy session provided by the unit of work."""

		self._session = session

	def add(self, asset: Asset) -> Asset:
		"""Insert a new asset row and return the persisted aggregate."""

		model = merge_asset_into_model(asset)
		self._session.add(model)
		self._session.flush()
		return asset_to_entity(model)

	def update(self, asset: Asset) -> Asset:
		"""Persist scalar field changes for an existing asset aggregate."""

		model = self._require_asset_model(asset.id)
		merge_asset_into_model(asset, model)
		self._session.flush()
		return asset_to_entity(model)

	def get_by_id(self, asset_id: int) -> Asset | None:
		"""Load one asset aggregate by identifier."""

		stmt = select(AssetModel).where(AssetModel.id == asset_id)
		model = self._session.scalar(stmt)
		return asset_to_entity(model) if model is not None else None

	def get_by_code(self, asset_code: str) -> Asset | None:
		"""Load one asset aggregate by its business code."""

		stmt = select(AssetModel).where(AssetModel.asset_code == asset_code)
		model = self._session.scalar(stmt)
		return asset_to_entity(model) if model is not None else None

	def list(self, *, status: str | None = None) -> Sequence[Asset]:
		"""Load asset aggregates with an optional status filter."""

		stmt = select(AssetModel).order_by(AssetModel.id)
		if status is not None:
			stmt = stmt.where(AssetModel.status == status)
		return [asset_to_entity(model) for model in self._session.scalars(stmt).all()]

	def delete(self, asset_id: int) -> None:
		"""Delete one asset row by identifier."""

		self._session.delete(self._require_asset_model(asset_id))

	def _require_asset_model(self, asset_id: int | None) -> AssetModel:
		"""Resolve one asset model or fail fast when the identifier is invalid."""

		if asset_id is None:
			raise ValueError("Asset id is required for this operation.")
		model = self._session.get(AssetModel, asset_id)
		if model is None:
			raise ValueError(f"Asset with id {asset_id} was not found.")
		return model
