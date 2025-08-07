import os
from typing import List, Optional
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from models import Customer, CustomerCreate, CustomerUpdate, generate_customer_id


class CosmosDBClient:
    """Azure Cosmos DB client for customer operations"""
    
    def __init__(self):
        self.cosmos_url = os.getenv("COSMOS_URL")
        self.cosmos_connection_string = os.getenv("COSMOS_CONNECTION_STRING")
        self.database_name = os.getenv("COSMOS_DATABASE")
        self.container_name = os.getenv("COSMOS_CONTAINER")
        
        if not all([self.cosmos_url, self.cosmos_connection_string, self.database_name, self.container_name]):
            raise ValueError("Missing required environment variables for Cosmos DB connection")
        
        # Initialize Cosmos client
        self.client = CosmosClient.from_connection_string(self.cosmos_connection_string)
        self.database: DatabaseProxy = self.client.get_database_client(self.database_name)
        self.container: ContainerProxy = self.database.get_container_client(self.container_name)
    
    async def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create a new customer"""
        customer_id = generate_customer_id()
        customer_dict = customer_data.model_dump()
        customer_dict["id"] = customer_id
        
        # Create the item in Cosmos DB
        created_item = self.container.create_item(body=customer_dict)
        return Customer(**created_item)
    
    async def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID"""
        try:
            item = self.container.read_item(item=customer_id, partition_key=customer_id)
            return Customer(**item)
        except CosmosResourceNotFoundError:
            return None
    
    async def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        query = "SELECT * FROM c"
        items = list(self.container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return [Customer(**item) for item in items]
    
    async def update_customer(self, customer_id: str, customer_update: CustomerUpdate) -> Optional[Customer]:
        """Update a customer"""
        try:
            # First, get the existing customer
            existing_item = self.container.read_item(item=customer_id, partition_key=customer_id)
            
            # Update only the fields that are provided
            update_data = customer_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                existing_item[key] = value
            
            # Replace the item in Cosmos DB
            updated_item = self.container.replace_item(item=customer_id, body=existing_item)
            return Customer(**updated_item)
        except CosmosResourceNotFoundError:
            return None
    
    async def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer"""
        try:
            self.container.delete_item(item=customer_id, partition_key=customer_id)
            return True
        except CosmosResourceNotFoundError:
            return False


# Global instance
_cosmos_client = None


def get_cosmos_client() -> CosmosDBClient:
    """Get the Cosmos DB client instance"""
    global _cosmos_client
    if _cosmos_client is None:
        _cosmos_client = CosmosDBClient()
    return _cosmos_client
