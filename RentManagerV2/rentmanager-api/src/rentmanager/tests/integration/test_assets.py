from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from rentmanager.main import app
from rentmanager.modules.assets.application.use_cases.manage_assets import ManageAssetsUseCase
from rentmanager.modules.assets.domain.entities import Asset
from rentmanager.modules.assets.interfaces.api.dependencies import get_manage_assets_use_case
from rentmanager.modules.iam.domain.entities import Functionality
from rentmanager.modules.iam.domain.entities import Role
from rentmanager.modules.iam.domain.entities import User
from rentmanager.modules.iam.interfaces.api.dependencies import get_current_username
from rentmanager.modules.iam.interfaces.api.dependencies import get_user_repository


class _FakeAssetRepository:
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


class _FakeUserRepository:
    def __init__(self, granted_codes: set[str]) -> None:
        functionalities = [
            Functionality(id=index + 1, code=code, name=code)
            for index, code in enumerate(sorted(granted_codes))
        ]
        role = Role(id=1, name="ADMIN", functionalities=functionalities)
        self._user = User(
            id=1,
            dni=None,
            username="admin",
            first_name="System",
            last_name="Admin",
            email="admin@local.dev",
            phone=None,
            password_hash="hash",
            is_active=True,
            roles=[role],
        )

    def get_by_username(self, username: str) -> User | None:
        if username == self._user.username:
            return self._user
        return None


@pytest.fixture
def client() -> TestClient:
    fake_repo = _FakeAssetRepository()
    use_case = ManageAssetsUseCase(asset_repository=fake_repo)

    app.dependency_overrides[get_manage_assets_use_case] = lambda: use_case
    app.dependency_overrides[get_current_username] = lambda: "admin"
    app.dependency_overrides[get_user_repository] = lambda: _FakeUserRepository(
        {"assets.read", "assets.write"}
    )

    client_instance = TestClient(app)
    try:
        yield client_instance
    finally:
        app.dependency_overrides.clear()


def test_assets_crud_flow(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/assets",
        json={
            "asset_code": "APT-001",
            "asset_type": "apartment",
            "name": "Apt 101",
            "address_line": "123 Main Street",
            "bedroom_count": 2,
            "rental_value": "850.00",
            "balance_favor": "0.00",
            "status": "available",
        },
    )

    assert create_response.status_code == 201
    created_payload = create_response.json()
    assert created_payload["id"] == 1
    assert created_payload["asset_code"] == "APT-001"

    list_response = client.get("/api/v1/assets")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get("/api/v1/assets/1")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Apt 101"

    update_response = client.patch(
        "/api/v1/assets/1",
        json={"status": "occupied", "balance_favor": "25.50"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "occupied"
    assert Decimal(update_response.json()["balance_favor"]) == Decimal("25.50")

    delete_response = client.delete("/api/v1/assets/1")
    assert delete_response.status_code == 204

    not_found_response = client.get("/api/v1/assets/1")
    assert not_found_response.status_code == 404


def test_assets_create_rejects_duplicate_code(client: TestClient) -> None:
    payload = {
        "asset_code": "APT-002",
        "asset_type": "studio",
        "name": "Apt 202",
        "address_line": "45 North Avenue",
        "bedroom_count": 1,
        "rental_value": "600.00",
        "balance_favor": "0.00",
        "status": "available",
    }

    first = client.post("/api/v1/assets", json=payload)
    second = client.post("/api/v1/assets", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_assets_forbidden_without_required_functionality(client: TestClient) -> None:
    app.dependency_overrides[get_user_repository] = lambda: _FakeUserRepository(set())

    response = client.get("/api/v1/assets")

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"
