from __future__ import annotations

from rentmanager.modules.assets.domain.entities import Asset
from rentmanager.modules.assets.infrastructure.models import AssetModel


def asset_to_entity(model: AssetModel) -> Asset:
	"""Translate one ORM asset row into a domain aggregate."""

	return Asset(
		id=model.id,
		asset_code=model.asset_code,
		asset_type=model.asset_type,
		name=model.name,
		address_line=model.address_line,
		bedroom_count=model.bedroom_count,
		rental_value=model.rental_value,
		balance_favor=model.balance_favor,
		status=model.status,
		created_at=model.created_at,
		updated_at=model.updated_at,
	)


def merge_asset_into_model(entity: Asset, model: AssetModel | None = None) -> AssetModel:
	"""Copy scalar domain fields into an ORM asset instance."""

	model = model or AssetModel()
	model.asset_code = entity.asset_code
	model.asset_type = entity.asset_type
	model.name = entity.name
	model.address_line = entity.address_line
	model.bedroom_count = entity.bedroom_count
	model.rental_value = entity.rental_value
	model.balance_favor = entity.balance_favor
	model.status = entity.status
	return model
