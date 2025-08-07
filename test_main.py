import pytest
from fastapi.testclient import TestClient
from main import app
from models import Customer, CustomerCreate, CustomerUpdate


class FakeRepo:
    def __init__(self):
        self.items: dict[str, Customer] = {}

    def list(self):
        return list(self.items.values())

    def get(self, customer_id: str):
        return self.items.get(customer_id)

    def create(self, data: CustomerCreate):
        c = Customer(**data.model_dump())
        self.items[c.id] = c
        return c

    def update(self, customer_id: str, data: CustomerUpdate):
        existing = self.get(customer_id)
        if not existing:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(existing, k, v)
        self.items[customer_id] = existing
        return existing

    def delete(self, customer_id: str):
        return self.items.pop(customer_id, None) is not None


@pytest.fixture()
def client():
    fake = FakeRepo()
    from main import get_repo

    def _get_repo():
        return fake

    app.dependency_overrides[get_repo] = _get_repo
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def test_crud_flow(client):
    # Create
    resp = client.post("/customers", json={"firstname": "John", "lastname": "Doe", "age": 30})
    assert resp.status_code == 201, resp.text
    created = resp.json()
    cid = created["id"]

    # Get
    resp = client.get(f"/customers/{cid}")
    assert resp.status_code == 200
    assert resp.json()["firstname"] == "John"

    # List
    resp = client.get("/customers")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Update
    resp = client.put(f"/customers/{cid}", json={"age": 31})
    assert resp.status_code == 200
    assert resp.json()["age"] == 31

    # Delete
    resp = client.delete(f"/customers/{cid}")
    assert resp.status_code == 204

    # Verify gone
    resp = client.get(f"/customers/{cid}")
    assert resp.status_code == 404
