from fastapi import Depends
from sqlalchemy.orm import Session

from rentmanager.modules.assets.domain.repositories import AssetRepository
from rentmanager.modules.assets.infrastructure.repositories_sqlalchemy import (
	SqlAlchemyAssetRepository,
)
from rentmanager.modules.contracts.application.use_cases.manage_contracts import (
	ManageContractsUseCase,
)
from rentmanager.modules.contracts.domain.repositories import ContractRepository
from rentmanager.modules.contracts.infrastructure.repositories_sqlalchemy import (
	SqlAlchemyContractRepository,
)
from rentmanager.modules.iam.domain.repositories import UserRepository
from rentmanager.modules.iam.infrastructure.repositories_sqlalchemy import SqlAlchemyUserRepository
from rentmanager.shared_kernel.infrastructure.db.session import get_db_session


def get_contract_repository(session: Session = Depends(get_db_session)) -> ContractRepository:
	return SqlAlchemyContractRepository(session=session)


def get_asset_repository(session: Session = Depends(get_db_session)) -> AssetRepository:
	return SqlAlchemyAssetRepository(session=session)


def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepository:
	return SqlAlchemyUserRepository(session=session)


def get_manage_contracts_use_case(
	contract_repository: ContractRepository = Depends(get_contract_repository),
	asset_repository: AssetRepository = Depends(get_asset_repository),
	user_repository: UserRepository = Depends(get_user_repository),
) -> ManageContractsUseCase:
	return ManageContractsUseCase(
		contract_repository=contract_repository,
		asset_repository=asset_repository,
		user_repository=user_repository,
	)
