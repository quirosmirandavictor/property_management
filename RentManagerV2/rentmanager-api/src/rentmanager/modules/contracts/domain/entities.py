from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class TenantContract:
	"""Domain representation of one tenant linked to a contract."""

	id: int | None
	contract_id: int
	user_id: int
	role_in_contract: str


@dataclass(slots=True)
class ContractDocument:
	"""Domain representation of one contract document metadata record."""

	id: int | None
	contract_id: int
	category: str
	original_filename: str
	content_type: str
	size_bytes: int
	blob_container: str
	blob_key: str
	uploaded_at: datetime | None = None


@dataclass(slots=True)
class Contract:
	"""Domain representation of a lease agreement aggregate."""

	id: int | None
	contract_code: str
	asset_id: int
	start_date: datetime
	end_date: datetime
	rent_amount: Decimal
	deposit_amount: Decimal
	status: str
	created_at: datetime | None = None
	updated_at: datetime | None = None
	tenant_contracts: list[TenantContract] = field(default_factory=list)
	documents: list[ContractDocument] = field(default_factory=list)
