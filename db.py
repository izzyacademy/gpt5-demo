import os
from typing import List, Optional
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from models import Customer, CustomerCreate, CustomerUpdate, apply_update  # type: ignore


def get_cosmos_client() -> CosmosClient:
    url = os.getenv("COSMOS_URL")
    conn = os.getenv("COSMOS_CONNECTION_STRING")
    if not url and not conn:
        raise RuntimeError("Missing Cosmos DB configuration (COSMOS_URL or COSMOS_CONNECTION_STRING)")
    if conn:
        return CosmosClient.from_connection_string(conn)
    assert url is not None
    return CosmosClient(url, credential=os.getenv("COSMOS_KEY"))


def get_container():
    client = get_cosmos_client()
    database_name = os.getenv("COSMOS_DATABASE")
    container_name = os.getenv("COSMOS_CONTAINER")
    if not database_name or not container_name:
        raise RuntimeError("Missing COSMOS_DATABASE or COSMOS_CONTAINER env vars")
    try:
        database = client.create_database_if_not_exists(id=database_name)
        container = database.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path="/id"))
        return container
    except exceptions.CosmosHttpResponseError as e:  # pragma: no cover
        raise RuntimeError(f"Cosmos error: {e}")


class CustomerRepository:
    def __init__(self):
        self._container = get_container()

    def list(self) -> List[Customer]:
        query = "SELECT * FROM c"
        items = list(self._container.query_items(query=query, enable_cross_partition_query=True))
        return [Customer(**item) for item in items]

    def get(self, customer_id: str) -> Optional[Customer]:
        try:
            item = self._container.read_item(item=customer_id, partition_key=customer_id)
            return Customer(**item)
        except exceptions.CosmosResourceNotFoundError:
            return None

    def create(self, data: CustomerCreate) -> Customer:
        customer = Customer(**data.model_dump())
        self._container.create_item(body=customer.model_dump())
        return customer

    def update(self, customer_id: str, data: CustomerUpdate) -> Optional[Customer]:
        existing = self.get(customer_id)
        if not existing:
            return None
        updated = apply_update(existing, data)
        self._container.replace_item(item=customer_id, body=updated.model_dump())
        return updated

    def delete(self, customer_id: str) -> bool:
        try:
            self._container.delete_item(item=customer_id, partition_key=customer_id)
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
