from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CreateContractInput:
	contract_code: str
	asset_id: int
	start_date: datetime
	end_date: datetime
	rent_amount: Decimal
	deposit_amount: Decimal
	status: str


@dataclass(frozen=True)
class CreateContractDocumentInput:
	contract_id: int
	category: str
	original_filename: str
	content_type: str
	size_bytes: int
	blob_container: str
	blob_key: str


@dataclass(frozen=True)
class TenantContractOutput:
	id: int | None
	contract_id: int
	user_id: int
	role_in_contract: str


@dataclass(frozen=True)
class ContractDocumentOutput:
	id: int | None
	contract_id: int
	category: str
	original_filename: str
	content_type: str
	size_bytes: int
	blob_container: str
	blob_key: str
	uploaded_at: datetime | None


@dataclass(frozen=True)
class ContractOutput:
	id: int
	contract_code: str
	asset_id: int
	start_date: datetime
	end_date: datetime
	rent_amount: Decimal
	deposit_amount: Decimal
	status: str
	created_at: datetime | None
	updated_at: datetime | None
	tenant_contracts: list[TenantContractOutput]
	documents: list[ContractDocumentOutput]
