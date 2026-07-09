from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from rentmanager.modules.assets.application.dtos import AssetOutput
from rentmanager.modules.assets.application.dtos import CreateAssetInput
from rentmanager.modules.assets.domain.entities import Asset
from rentmanager.modules.assets.domain.exceptions import AssetCodeAlreadyExistsError
from rentmanager.modules.assets.domain.exceptions import AssetNotFoundError
from rentmanager.modules.assets.domain.exceptions import InvalidAssetStateError
from rentmanager.modules.assets.domain.repositories import AssetRepository

_ALLOWED_ASSET_STATUSES = {"available", "occupied", "maintenance", "inactive"}


class ManageAssetsUseCase:
	"""Orchestrate asset CRUD use cases over the repository abstraction."""

	def __init__(self, asset_repository: AssetRepository) -> None:
		self._asset_repository = asset_repository

	def create(self, payload: CreateAssetInput) -> AssetOutput:
		if self._asset_repository.get_by_code(payload.asset_code) is not None:
			raise AssetCodeAlreadyExistsError("Asset code is already registered.")

		asset = Asset(
			id=None,
			asset_code=payload.asset_code,
			asset_type=payload.asset_type,
			name=payload.name,
			address_line=payload.address_line,
			bedroom_count=payload.bedroom_count,
			rental_value=payload.rental_value,
			balance_favor=payload.balance_favor,
			status=payload.status,
		)
		self._validate_asset(asset)

		persisted = self._asset_repository.add(asset)
		return self._to_output(persisted)

	def get(self, asset_id: int) -> AssetOutput:
		asset = self._asset_repository.get_by_id(asset_id)
		if asset is None:
			raise AssetNotFoundError(f"Asset with id {asset_id} was not found.")
		return self._to_output(asset)

	def list(self, *, status: str | None = None) -> Sequence[AssetOutput]:
		if status is not None and status not in _ALLOWED_ASSET_STATUSES:
			raise InvalidAssetStateError("Asset status filter is invalid.")
		return [self._to_output(asset) for asset in self._asset_repository.list(status=status)]

	def update(self, asset_id: int, updates: Mapping[str, Any]) -> AssetOutput:
		current = self._asset_repository.get_by_id(asset_id)
		if current is None:
			raise AssetNotFoundError(f"Asset with id {asset_id} was not found.")

		if "asset_code" in updates:
			asset_code = updates["asset_code"]
			if isinstance(asset_code, str) and asset_code != current.asset_code:
				by_code = self._asset_repository.get_by_code(asset_code)
				if by_code is not None and by_code.id != current.id:
					raise AssetCodeAlreadyExistsError("Asset code is already registered.")

		for field_name, field_value in updates.items():
			if hasattr(current, field_name):
				setattr(current, field_name, field_value)

		self._validate_asset(current)
		updated = self._asset_repository.update(current)
		return self._to_output(updated)

	def delete(self, asset_id: int) -> None:
		if self._asset_repository.get_by_id(asset_id) is None:
			raise AssetNotFoundError(f"Asset with id {asset_id} was not found.")
		self._asset_repository.delete(asset_id)

	def _validate_asset(self, asset: Asset) -> None:
		if asset.status not in _ALLOWED_ASSET_STATUSES:
			raise InvalidAssetStateError(
				"Asset status must be one of: available, occupied, maintenance, inactive."
			)
		if asset.bedroom_count is not None and asset.bedroom_count < 0:
			raise InvalidAssetStateError("Bedroom count cannot be negative.")
		if asset.rental_value < Decimal("0"):
			raise InvalidAssetStateError("Rental value cannot be negative.")

	def _to_output(self, asset: Asset) -> AssetOutput:
		if asset.id is None:
			raise InvalidAssetStateError("Asset identity is invalid.")
		return AssetOutput(
			id=asset.id,
			asset_code=asset.asset_code,
			asset_type=asset.asset_type,
			name=asset.name,
			address_line=asset.address_line,
			bedroom_count=asset.bedroom_count,
			rental_value=asset.rental_value,
			balance_favor=asset.balance_favor,
			status=asset.status,
			created_at=asset.created_at,
			updated_at=asset.updated_at,
		)
