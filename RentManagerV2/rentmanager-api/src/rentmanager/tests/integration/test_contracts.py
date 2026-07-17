from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from rentmanager.main import app
from rentmanager.modules.assets.domain.entities import Asset
from rentmanager.modules.contracts.application.use_cases.manage_contracts import (
    ManageContractsUseCase,
)
from rentmanager.modules.contracts.domain.entities import Contract, ContractDocument, TenantContract
from rentmanager.modules.contracts.interfaces.api.dependencies import get_manage_contracts_use_case
from rentmanager.modules.iam.domain.entities import Functionality, Role, User
from rentmanager.modules.iam.interfaces.api.dependencies import (
    get_current_username,
    get_user_repository,
)


class _FakeAssetRepository:
    def __init__(self) -> None:
        self._assets: dict[int, Asset] = {
            1: Asset(
                id=1,
                asset_code="APT-001",
                asset_type="apartment",
                name="Apt 101",
                address_line="123 Main Street",
                bedroom_count=2,
                rental_value=Decimal("850.00"),
                balance_favor=Decimal("0.00"),
                status="available",
            )
        }

    def get_by_id(self, asset_id: int) -> Asset | None:
        return self._assets.get(asset_id)


class _FakeContractRepository:
    def __init__(self) -> None:
        self._items: dict[int, Contract] = {}
        self._next_contract_id = 1
        self._next_tenant_id = 1
        self._next_document_id = 1

    def add(self, contract: Contract) -> Contract:
        persisted = Contract(
            id=self._next_contract_id,
            contract_code=contract.contract_code,
            asset_id=contract.asset_id,
            start_date=contract.start_date,
            end_date=contract.end_date,
            rent_amount=contract.rent_amount,
            deposit_amount=contract.deposit_amount,
            status=contract.status,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            tenant_contracts=[],
            documents=[],
        )
        self._items[persisted.id] = persisted
        self._next_contract_id += 1
        return persisted

    def update(self, contract: Contract) -> Contract:
        assert contract.id is not None
        contract.updated_at = datetime.now(UTC)
        self._items[contract.id] = contract
        return contract

    def get_by_id(self, contract_id: int) -> Contract | None:
        return self._items.get(contract_id)

    def get_by_code(self, contract_code: str) -> Contract | None:
        return next(
            (item for item in self._items.values() if item.contract_code == contract_code),
            None,
        )

    def list(self, *, asset_id: int | None = None, status: str | None = None):
        items = list(self._items.values())
        if asset_id is not None:
            items = [item for item in items if item.asset_id == asset_id]
        if status is not None:
            items = [item for item in items if item.status == status]
        return items

    def list_by_asset(self, asset_id: int):
        return self.list(asset_id=asset_id)

    def add_tenant(self, contract_id: int, user_id: int, role_in_contract: str) -> None:
        contract = self._items[contract_id]
        contract.tenant_contracts.append(
            TenantContract(
                id=self._next_tenant_id,
                contract_id=contract_id,
                user_id=user_id,
                role_in_contract=role_in_contract,
            )
        )
        self._next_tenant_id += 1

    def remove_tenant(self, contract_id: int, user_id: int) -> None:
        contract = self._items[contract_id]
        contract.tenant_contracts = [
            item for item in contract.tenant_contracts if item.user_id != user_id
        ]

    def add_document(self, document: ContractDocument) -> ContractDocument:
        persisted = ContractDocument(
            id=self._next_document_id,
            contract_id=document.contract_id,
            category=document.category,
            original_filename=document.original_filename,
            content_type=document.content_type,
            size_bytes=document.size_bytes,
            blob_container=document.blob_container,
            blob_key=document.blob_key,
            uploaded_at=datetime.now(UTC),
        )
        self._items[document.contract_id].documents.append(persisted)
        self._next_document_id += 1
        return persisted

    def remove_document(self, document_id: int) -> None:
        for contract in self._items.values():
            contract.documents = [item for item in contract.documents if item.id != document_id]

    def delete(self, contract_id: int) -> None:
        self._items.pop(contract_id, None)


class _FakeUserRepository:
    def __init__(self, granted_codes: set[str], existing_user_ids: set[int]) -> None:
        functionalities = [
            Functionality(id=index + 1, code=code, name=code)
            for index, code in enumerate(sorted(granted_codes))
        ]
        role = Role(id=1, name="ADMIN", functionalities=functionalities)
        self._auth_user = User(
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
        self._existing_user_ids = existing_user_ids

    def get_by_username(self, username: str) -> User | None:
        if username == self._auth_user.username:
            return self._auth_user
        return None

    def get_by_id(self, user_id: int) -> User | None:
        if user_id in self._existing_user_ids:
            return self._auth_user
        return None


@pytest.fixture
def client() -> TestClient:
    fake_contract_repo = _FakeContractRepository()
    fake_asset_repo = _FakeAssetRepository()
    fake_user_repo = _FakeUserRepository({"contracts.read", "contracts.write"}, {1, 2})

    use_case = ManageContractsUseCase(
        contract_repository=fake_contract_repo,
        asset_repository=fake_asset_repo,
        user_repository=fake_user_repo,
    )

    app.dependency_overrides[get_manage_contracts_use_case] = lambda: use_case
    app.dependency_overrides[get_current_username] = lambda: "admin"
    app.dependency_overrides[get_user_repository] = lambda: fake_user_repo

    client_instance = TestClient(app)
    try:
        yield client_instance
    finally:
        app.dependency_overrides.clear()


def test_contracts_crud_and_blob_reference_flow(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/contracts",
        json={
            "contract_code": "CTR-2026-001",
            "asset_id": 1,
            "start_date": "2026-07-01T00:00:00Z",
            "end_date": "2027-06-30T00:00:00Z",
            "rent_amount": "900.00",
            "deposit_amount": "900.00",
            "status": "active",
        },
    )

    assert create_response.status_code == 201
    payload = create_response.json()
    assert payload["id"] == 1
    assert payload["contract_code"] == "CTR-2026-001"

    list_response = client.get("/api/v1/contracts")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    tenant_response = client.post(
        "/api/v1/contracts/1/tenants",
        json={"user_id": 2, "role_in_contract": "tenant"},
    )
    assert tenant_response.status_code == 200
    assert len(tenant_response.json()["tenant_contracts"]) == 1

    add_document_response = client.post(
        "/api/v1/contracts/1/documents",
        json={
            "category": "signed_contract",
            "original_filename": "contract-2026.pdf",
            "content_type": "application/pdf",
            "size_bytes": 1048576,
            "blob_container": "contracts",
            "blob_key": "contracts/CTR-2026-001/signed/contract-2026.pdf",
        },
    )
    assert add_document_response.status_code == 200
    document_payload = add_document_response.json()["documents"][0]
    assert document_payload["blob_container"] == "contracts"
    assert document_payload["blob_key"].endswith("contract-2026.pdf")

    remove_document_response = client.delete("/api/v1/contracts/1/documents/1")
    assert remove_document_response.status_code == 200
    assert remove_document_response.json()["documents"] == []

    delete_response = client.delete("/api/v1/contracts/1")
    assert delete_response.status_code == 204

    not_found_response = client.get("/api/v1/contracts/1")
    assert not_found_response.status_code == 404


def test_contracts_forbidden_without_required_functionality(client: TestClient) -> None:
    app.dependency_overrides[get_user_repository] = lambda: _FakeUserRepository(set(), {1, 2})

    response = client.get("/api/v1/contracts")

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"
