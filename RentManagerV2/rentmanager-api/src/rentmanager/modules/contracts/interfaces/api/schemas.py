from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TenantContractResponse(BaseModel):
	id: int | None
	contract_id: int
	user_id: int
	role_in_contract: str


class ContractDocumentResponse(BaseModel):
	id: int | None
	contract_id: int
	category: str
	original_filename: str
	content_type: str
	size_bytes: int
	blob_container: str
	blob_key: str
	uploaded_at: datetime | None


class ContractResponse(BaseModel):
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
	tenant_contracts: list[TenantContractResponse]
	documents: list[ContractDocumentResponse]


class CreateContractRequest(BaseModel):
	contract_code: str = Field(min_length=2, max_length=50)
	asset_id: int = Field(gt=0)
	start_date: datetime
	end_date: datetime
	rent_amount: Decimal = Field(ge=0)
	deposit_amount: Decimal = Field(default=Decimal("0"), ge=0)
	status: str = Field(default="draft", min_length=3, max_length=50)


class UpdateContractRequest(BaseModel):
	contract_code: str | None = Field(default=None, min_length=2, max_length=50)
	asset_id: int | None = Field(default=None, gt=0)
	start_date: datetime | None = None
	end_date: datetime | None = None
	rent_amount: Decimal | None = Field(default=None, ge=0)
	deposit_amount: Decimal | None = Field(default=None, ge=0)
	status: str | None = Field(default=None, min_length=3, max_length=50)


class AddTenantRequest(BaseModel):
	user_id: int = Field(gt=0)
	role_in_contract: str = Field(default="tenant", min_length=3, max_length=50)


class AddContractDocumentRequest(BaseModel):
	category: str = Field(min_length=2, max_length=50)
	original_filename: str = Field(min_length=1, max_length=255)
	content_type: str = Field(min_length=3, max_length=100)
	size_bytes: int = Field(gt=0)
	blob_container: str = Field(min_length=3, max_length=100)
	blob_key: str = Field(min_length=3, max_length=255)
