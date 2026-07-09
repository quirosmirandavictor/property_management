from __future__ import annotations

from decimal import Decimal

import pytest

from rentmanager.modules.assets.application.dtos import CreateAssetInput
from rentmanager.modules.assets.application.use_cases.manage_assets import ManageAssetsUseCase
from rentmanager.modules.assets.domain.entities import Asset
from rentmanager.modules.assets.domain.exceptions import AssetCodeAlreadyExistsError
from rentmanager.modules.assets.domain.exceptions import AssetNotFoundError
from rentmanager.modules.assets.domain.exceptions import InvalidAssetStateError


class _InMemoryAssetRepository:
    def __init__(self) -> None:
        self._items: dict[int, Asset] = {}
        self._next_id = 1

    def add(self, asset: Asset) -> Asset:
        persisted = Asset(
            id=self._next_id,
            asset_code=asset.asset_code,
            asset_type=asset.asset_type,
            name=asset.name,
            address_line=asset.address_line,
            bedroom_count=asset.bedroom_count,
            rental_value=asset.rental_value,
            balance_favor=asset.balance_favor,
            status=asset.status,
        )
        self._items[self._next_id] = persisted
        self._next_id += 1
        return persisted

    def update(self, asset: Asset) -> Asset:
        assert asset.id is not None
        self._items[asset.id] = asset
        return asset

    def get_by_id(self, asset_id: int) -> Asset | None:
        return self._items.get(asset_id)

    def get_by_code(self, asset_code: str) -> Asset | None:
        return next((item for item in self._items.values() if item.asset_code == asset_code), None)

    def list(self, *, status: str | None = None):
        items = list(self._items.values())
        if status is not None:
            items = [item for item in items if item.status == status]
        return items

    def delete(self, asset_id: int) -> None:
        self._items.pop(asset_id, None)


@pytest.fixture
def use_case() -> ManageAssetsUseCase:
    return ManageAssetsUseCase(asset_repository=_InMemoryAssetRepository())


def test_create_asset_success(use_case: ManageAssetsUseCase) -> None:
    output = use_case.create(
        CreateAssetInput(
            asset_code="HSE-001",
            asset_type="house",
            name="House 1",
            address_line="1 Ocean Avenue",
            bedroom_count=3,
            rental_value=Decimal("1200.00"),
            balance_favor=Decimal("0.00"),
            status="available",
        )
    )

    assert output.id == 1
    assert output.asset_code == "HSE-001"


def test_create_asset_rejects_duplicate_code(use_case: ManageAssetsUseCase) -> None:
    payload = CreateAssetInput(
        asset_code="DUP-001",
        asset_type="apartment",
        name="Apt 404",
        address_line="404 East Street",
        bedroom_count=1,
        rental_value=Decimal("700.00"),
        balance_favor=Decimal("0.00"),
        status="available",
    )

    use_case.create(payload)

    with pytest.raises(AssetCodeAlreadyExistsError):
        use_case.create(payload)


def test_create_asset_rejects_invalid_status(use_case: ManageAssetsUseCase) -> None:
    with pytest.raises(InvalidAssetStateError):
        use_case.create(
            CreateAssetInput(
                asset_code="BAD-001",
                asset_type="apartment",
                name="Apt Invalid",
                address_line="Invalid Address",
                bedroom_count=1,
                rental_value=Decimal("700.00"),
                balance_favor=Decimal("0.00"),
                status="unknown",
            )
        )


def test_get_asset_not_found(use_case: ManageAssetsUseCase) -> None:
    with pytest.raises(AssetNotFoundError):
        use_case.get(99)


def test_update_asset_rejects_negative_rental_value(use_case: ManageAssetsUseCase) -> None:
    created = use_case.create(
        CreateAssetInput(
            asset_code="UPD-001",
            asset_type="apartment",
            name="Apt Update",
            address_line="25 Main Street",
            bedroom_count=2,
            rental_value=Decimal("900.00"),
            balance_favor=Decimal("0.00"),
            status="available",
        )
    )

    with pytest.raises(InvalidAssetStateError):
        use_case.update(created.id, {"rental_value": Decimal("-1")})


def test_list_assets_by_status(use_case: ManageAssetsUseCase) -> None:
    use_case.create(
        CreateAssetInput(
            asset_code="LST-001",
            asset_type="house",
            name="House Available",
            address_line="1 Blue Street",
            bedroom_count=2,
            rental_value=Decimal("950.00"),
            balance_favor=Decimal("0.00"),
            status="available",
        )
    )
    use_case.create(
        CreateAssetInput(
            asset_code="LST-002",
            asset_type="house",
            name="House Occupied",
            address_line="2 Blue Street",
            bedroom_count=2,
            rental_value=Decimal("980.00"),
            balance_favor=Decimal("0.00"),
            status="occupied",
        )
    )

    available_items = use_case.list(status="available")

    assert len(available_items) == 1
    assert available_items[0].asset_code == "LST-001"


def test_delete_asset_not_found(use_case: ManageAssetsUseCase) -> None:
    with pytest.raises(AssetNotFoundError):
        use_case.delete(777)
