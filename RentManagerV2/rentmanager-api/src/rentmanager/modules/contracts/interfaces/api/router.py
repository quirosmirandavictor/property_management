from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from rentmanager.modules.contracts.application.dtos import (
	CreateContractDocumentInput,
	CreateContractInput,
)
from rentmanager.modules.contracts.application.use_cases.manage_contracts import (
	ManageContractsUseCase,
)
from rentmanager.modules.contracts.domain.exceptions import (
	ContractCodeAlreadyExistsError,
	ContractNotFoundError,
	ContractTenantAlreadyAssignedError,
	ContractTenantNotFoundError,
	InvalidContractStateError,
)
from rentmanager.modules.contracts.interfaces.api.dependencies import get_manage_contracts_use_case
from rentmanager.modules.contracts.interfaces.api.schemas import (
	AddContractDocumentRequest,
	AddTenantRequest,
	ContractResponse,
	CreateContractRequest,
	UpdateContractRequest,
)
from rentmanager.modules.iam.interfaces.api.dependencies import require_functionality

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.post(
	"",
	response_model=ContractResponse,
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Create contract",
	description="Create one lease contract and store only document references in MySQL.",
	responses={
		201: {"description": "Contract created."},
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		409: {"description": "Contract code already exists."},
		422: {"description": "Invalid contract payload."},
	},
)
def create_contract(
	payload: CreateContractRequest,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	try:
		created = use_case.create(
			CreateContractInput(
				contract_code=payload.contract_code,
				asset_id=payload.asset_id,
				start_date=payload.start_date,
				end_date=payload.end_date,
				rent_amount=payload.rent_amount,
				deposit_amount=payload.deposit_amount,
				status=payload.status,
			)
		)
		return ContractResponse.model_validate(created, from_attributes=True)
	except ContractCodeAlreadyExistsError as exc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
	except InvalidContractStateError as exc:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(exc),
		) from exc


@router.get(
	"",
	response_model=list[ContractResponse],
	dependencies=[Depends(require_functionality("contracts.read"))],
	summary="List contracts",
	description="List contracts with optional filters by asset and status.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.read functionality."},
		422: {"description": "Invalid filter values."},
	},
)
def list_contracts(
	asset_id: int | None = Query(default=None, ge=1),
	status_filter: str | None = Query(default=None, alias="status"),
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> list[ContractResponse]:
	try:
		items = use_case.list(asset_id=asset_id, status=status_filter)
		return [ContractResponse.model_validate(item, from_attributes=True) for item in items]
	except InvalidContractStateError as exc:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(exc),
		) from exc


@router.get(
	"/{contract_id}",
	response_model=ContractResponse,
	dependencies=[Depends(require_functionality("contracts.read"))],
	summary="Get contract by id",
	description="Retrieve one contract aggregate by identifier.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.read functionality."},
		404: {"description": "Contract not found."},
	},
)
def get_contract(
	contract_id: int,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	try:
		return ContractResponse.model_validate(use_case.get(contract_id), from_attributes=True)
	except ContractNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch(
	"/{contract_id}",
	response_model=ContractResponse,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Update contract",
	description="Apply partial updates to one existing contract.",
	responses={
		400: {"description": "No fields were provided to update."},
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		404: {"description": "Contract not found."},
		409: {"description": "Contract code already exists."},
		422: {"description": "Invalid updated values."},
	},
)
def update_contract(
	contract_id: int,
	payload: UpdateContractRequest,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	updates = payload.model_dump(exclude_unset=True)
	if not updates:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="At least one field is required to update a contract.",
		)

	try:
		updated = use_case.update(contract_id=contract_id, updates=updates)
		return ContractResponse.model_validate(updated, from_attributes=True)
	except ContractNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	except ContractCodeAlreadyExistsError as exc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
	except InvalidContractStateError as exc:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(exc),
		) from exc


@router.delete(
	"/{contract_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Delete contract",
	description="Delete one contract by identifier.",
	responses={
		204: {"description": "Contract deleted."},
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		404: {"description": "Contract not found."},
	},
)
def delete_contract(
	contract_id: int,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> Response:
	try:
		use_case.delete(contract_id)
	except ContractNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
	"/{contract_id}/tenants",
	response_model=ContractResponse,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Attach tenant to contract",
	description="Link one IAM user to one contract as tenant, co-tenant, or guarantor.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		404: {"description": "Contract not found."},
		409: {"description": "Tenant already assigned."},
		422: {"description": "Invalid tenant assignment payload."},
	},
)
def add_contract_tenant(
	contract_id: int,
	payload: AddTenantRequest,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	try:
		updated = use_case.add_tenant(
			contract_id=contract_id,
			user_id=payload.user_id,
			role_in_contract=payload.role_in_contract,
		)
		return ContractResponse.model_validate(updated, from_attributes=True)
	except ContractNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	except ContractTenantAlreadyAssignedError as exc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
	except InvalidContractStateError as exc:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(exc),
		) from exc


@router.delete(
	"/{contract_id}/tenants/{user_id}",
	response_model=ContractResponse,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Remove tenant from contract",
	description="Unlink one IAM user from one contract tenant assignment.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		404: {"description": "Contract or tenant assignment not found."},
	},
)
def remove_contract_tenant(
	contract_id: int,
	user_id: int,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	try:
		updated = use_case.remove_tenant(contract_id=contract_id, user_id=user_id)
		return ContractResponse.model_validate(updated, from_attributes=True)
	except (ContractNotFoundError, ContractTenantNotFoundError) as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
	"/{contract_id}/documents",
	response_model=ContractResponse,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Register contract document reference",
	description=(
		"Store contract file metadata and Azure Blob reference in MySQL. "
		"Binary document content is not persisted in relational tables."
	),
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		404: {"description": "Contract not found."},
		422: {"description": "Invalid document metadata payload."},
	},
)
def add_contract_document(
	contract_id: int,
	payload: AddContractDocumentRequest,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	try:
		updated = use_case.add_document(
			CreateContractDocumentInput(
				contract_id=contract_id,
				category=payload.category,
				original_filename=payload.original_filename,
				content_type=payload.content_type,
				size_bytes=payload.size_bytes,
				blob_container=payload.blob_container,
				blob_key=payload.blob_key,
			)
		)
		return ContractResponse.model_validate(updated, from_attributes=True)
	except ContractNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	except InvalidContractStateError as exc:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(exc),
		) from exc


@router.delete(
	"/{contract_id}/documents/{document_id}",
	response_model=ContractResponse,
	dependencies=[Depends(require_functionality("contracts.write"))],
	summary="Remove contract document reference",
	description="Delete one contract document metadata reference from MySQL.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing contracts.write functionality."},
		404: {"description": "Contract not found."},
		422: {"description": "Contract document was not found."},
	},
)
def remove_contract_document(
	contract_id: int,
	document_id: int,
	use_case: ManageContractsUseCase = Depends(get_manage_contracts_use_case),
) -> ContractResponse:
	try:
		updated = use_case.remove_document(contract_id=contract_id, document_id=document_id)
		return ContractResponse.model_validate(updated, from_attributes=True)
	except ContractNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	except InvalidContractStateError as exc:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(exc),
		) from exc
