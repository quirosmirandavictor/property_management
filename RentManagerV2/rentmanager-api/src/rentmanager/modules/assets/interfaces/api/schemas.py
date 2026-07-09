from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class AssetResponse(BaseModel):
	id: int
	asset_code: str
	asset_type: str
	name: str
	address_line: str
	bedroom_count: int | None
	rental_value: Decimal
	balance_favor: Decimal
	status: str
	created_at: datetime | None
	updated_at: datetime | None


class CreateAssetRequest(BaseModel):
	asset_code: str = Field(min_length=2, max_length=50)
	asset_type: str = Field(min_length=2, max_length=100)
	name: str = Field(min_length=2, max_length=150)
	address_line: str = Field(min_length=5, max_length=255)
	bedroom_count: int | None = Field(default=None, ge=0)
	rental_value: Decimal = Field(ge=0)
	balance_favor: Decimal = Field(default=Decimal("0"))
	status: str = Field(default="available", min_length=3, max_length=50)


class UpdateAssetRequest(BaseModel):
	asset_code: str | None = Field(default=None, min_length=2, max_length=50)
	asset_type: str | None = Field(default=None, min_length=2, max_length=100)
	name: str | None = Field(default=None, min_length=2, max_length=150)
	address_line: str | None = Field(default=None, min_length=5, max_length=255)
	bedroom_count: int | None = Field(default=None, ge=0)
	rental_value: Decimal | None = Field(default=None, ge=0)
	balance_favor: Decimal | None = None
	status: str | None = Field(default=None, min_length=3, max_length=50)
