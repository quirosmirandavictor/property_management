from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from rentmanager.modules.assets.application.dtos import CreateAssetInput
from rentmanager.modules.assets.application.use_cases.manage_assets import (
	ManageAssetsUseCase,
)
from rentmanager.modules.assets.domain.exceptions import AssetCodeAlreadyExistsError
from rentmanager.modules.assets.domain.exceptions import AssetNotFoundError
from rentmanager.modules.assets.domain.exceptions import InvalidAssetStateError
from rentmanager.modules.assets.interfaces.api.dependencies import get_manage_assets_use_case
from rentmanager.modules.assets.interfaces.api.schemas import AssetResponse
from rentmanager.modules.assets.interfaces.api.schemas import CreateAssetRequest
from rentmanager.modules.assets.interfaces.api.schemas import UpdateAssetRequest
from rentmanager.modules.iam.interfaces.api.dependencies import require_functionality

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post(
	"",
	response_model=AssetResponse,
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(require_functionality("assets.write"))],
	summary="Create asset",
	description="Create one new rentable asset record.",
	responses={
		201: {"description": "Asset created."},
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing assets.write functionality."},
		409: {"description": "Asset code already exists."},
		422: {"description": "Invalid asset payload."},
	},
)
def create_asset(
	payload: CreateAssetRequest,
	use_case: ManageAssetsUseCase = Depends(get_manage_assets_use_case),
) -> AssetResponse:
	try:
		created = use_case.create(
			CreateAssetInput(
				asset_code=payload.asset_code,
				asset_type=payload.asset_type,
				name=payload.name,
				address_line=payload.address_line,
				bedroom_count=payload.bedroom_count,
				rental_value=payload.rental_value,
				balance_favor=payload.balance_favor,
				status=payload.status,
			)
		)
		return AssetResponse.model_validate(created, from_attributes=True)
	except AssetCodeAlreadyExistsError as exc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
	except InvalidAssetStateError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get(
	"",
	response_model=list[AssetResponse],
	dependencies=[Depends(require_functionality("assets.read"))],
	summary="List assets",
	description="List all assets or filter by status.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing assets.read functionality."},
		422: {"description": "Invalid status filter."},
	},
)
def list_assets(
	status_filter: str | None = Query(default=None, alias="status"),
	use_case: ManageAssetsUseCase = Depends(get_manage_assets_use_case),
) -> list[AssetResponse]:
	try:
		items = use_case.list(status=status_filter)
		return [AssetResponse.model_validate(item, from_attributes=True) for item in items]
	except InvalidAssetStateError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get(
	"/{asset_id}",
	response_model=AssetResponse,
	dependencies=[Depends(require_functionality("assets.read"))],
	summary="Get asset by id",
	description="Retrieve one asset by its identifier.",
	responses={
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing assets.read functionality."},
		404: {"description": "Asset not found."},
	},
)
def get_asset(
	asset_id: int,
	use_case: ManageAssetsUseCase = Depends(get_manage_assets_use_case),
) -> AssetResponse:
	try:
		return AssetResponse.model_validate(use_case.get(asset_id), from_attributes=True)
	except AssetNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch(
	"/{asset_id}",
	response_model=AssetResponse,
	dependencies=[Depends(require_functionality("assets.write"))],
	summary="Update asset",
	description="Apply partial updates to one existing asset.",
	responses={
		400: {"description": "No fields were provided to update."},
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing assets.write functionality."},
		404: {"description": "Asset not found."},
		409: {"description": "Asset code already exists."},
		422: {"description": "Invalid updated values."},
	},
)
def update_asset(
	asset_id: int,
	payload: UpdateAssetRequest,
	use_case: ManageAssetsUseCase = Depends(get_manage_assets_use_case),
) -> AssetResponse:
	updates = payload.model_dump(exclude_unset=True)
	if not updates:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="At least one field is required to update an asset.",
		)

	try:
		updated = use_case.update(asset_id=asset_id, updates=updates)
		return AssetResponse.model_validate(updated, from_attributes=True)
	except AssetNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	except AssetCodeAlreadyExistsError as exc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
	except InvalidAssetStateError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.delete(
	"/{asset_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(require_functionality("assets.write"))],
	summary="Delete asset",
	description="Delete one asset by identifier.",
	responses={
		204: {"description": "Asset deleted."},
		401: {"description": "Missing or invalid access token."},
		403: {"description": "Missing assets.write functionality."},
		404: {"description": "Asset not found."},
	},
)
def delete_asset(
	asset_id: int,
	use_case: ManageAssetsUseCase = Depends(get_manage_assets_use_case),
) -> Response:
	try:
		use_case.delete(asset_id)
	except AssetNotFoundError as exc:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
	return Response(status_code=status.HTTP_204_NO_CONTENT)
