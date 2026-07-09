from fastapi import Depends
from sqlalchemy.orm import Session

from rentmanager.modules.assets.application.use_cases.manage_assets import (
	ManageAssetsUseCase,
)
from rentmanager.modules.assets.domain.repositories import AssetRepository
from rentmanager.modules.assets.infrastructure.repositories_sqlalchemy import (
	SqlAlchemyAssetRepository,
)
from rentmanager.shared_kernel.infrastructure.db.session import get_db_session


def get_asset_repository(session: Session = Depends(get_db_session)) -> AssetRepository:
	return SqlAlchemyAssetRepository(session=session)


def get_manage_assets_use_case(
	asset_repository: AssetRepository = Depends(get_asset_repository),
) -> ManageAssetsUseCase:
	return ManageAssetsUseCase(asset_repository=asset_repository)
