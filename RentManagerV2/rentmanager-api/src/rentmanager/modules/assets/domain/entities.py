from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class Asset:
	"""Domain representation of a rentable property or unit."""

	id: int | None
	asset_code: str
	asset_type: str
	name: str
	address_line: str
	bedroom_count: int | None
	rental_value: Decimal
	balance_favor: Decimal
	status: str
	created_at: datetime | None = None
	updated_at: datetime | None = None
