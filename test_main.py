import pytest
import os
import uuid
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from main import app
from models import Customer, CustomerCreate, CustomerUpdate
from db import CosmosDBClient


# Test client for FastAPI
client = TestClient(app)


class TestModels:
    """Test Pydantic models"""
    
    def test_customer_create_valid(self):
        """Test valid customer creation data"""
        customer_data = {
            "firstname": "John",
            "lastname": "Doe",
            "age": 30
        }
        customer = CustomerCreate(**customer_data)
        assert customer.firstname == "John"
        assert customer.lastname == "Doe"
        assert customer.age == 30
    
    def test_customer_create_invalid_age(self):
        """Test invalid age in customer creation"""
        with pytest.raises(ValueError):
            CustomerCreate(firstname="John", lastname="Doe", age=-1)
        
        with pytest.raises(ValueError):
            CustomerCreate(firstname="John", lastname="Doe", age=200)
    
    def test_customer_create_invalid_name(self):
        """Test invalid names in customer creation"""
        with pytest.raises(ValueError):
            CustomerCreate(firstname="", lastname="Doe", age=30)
        
        with pytest.raises(ValueError):
            CustomerCreate(firstname="John", lastname="", age=30)
    
    def test_customer_update_partial(self):
        """Test partial customer update"""
        update_data = {"firstname": "Jane"}
        customer_update = CustomerUpdate(**update_data)
        assert customer_update.firstname == "Jane"
        assert customer_update.lastname is None
        assert customer_update.age is None
    
    def test_customer_model_with_id(self):
        """Test complete customer model"""
        customer_data = {
            "id": "test-id-123",
            "firstname": "John",
            "lastname": "Doe",
            "age": 30
        }
        customer = Customer(**customer_data)
        assert customer.id == "test-id-123"
        assert customer.firstname == "John"
        assert customer.lastname == "Doe"
        assert customer.age == 30


class TestCosmosDBClient:
    """Test Cosmos DB client operations"""
    
    @patch.dict(os.environ, {
        "COSMOS_URL": "https://test.documents.azure.com:443/",
        "COSMOS_CONNECTION_STRING": "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test==;",
        "COSMOS_DATABASE": "test_db",
        "COSMOS_CONTAINER": "test_container"
    })
    @patch('db.CosmosClient')
    def test_cosmos_client_initialization(self, mock_cosmos_client):
        """Test Cosmos DB client initialization"""
        mock_client_instance = Mock()
        mock_database = Mock()
        mock_container = Mock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        cosmos_client = CosmosDBClient()
        
        assert cosmos_client.cosmos_url == "https://test.documents.azure.com:443/"
        assert cosmos_client.database_name == "test_db"
        assert cosmos_client.container_name == "test_container"
        mock_cosmos_client.from_connection_string.assert_called_once()
    
    def test_cosmos_client_missing_env_vars(self):
        """Test Cosmos DB client with missing environment variables"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Missing required environment variables"):
                CosmosDBClient()
    
    @patch.dict(os.environ, {
        "COSMOS_URL": "https://test.documents.azure.com:443/",
        "COSMOS_CONNECTION_STRING": "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test==;",
        "COSMOS_DATABASE": "test_db",
        "COSMOS_CONTAINER": "test_container"
    })
    @patch('db.CosmosClient')
    @pytest.mark.asyncio
    async def test_create_customer(self, mock_cosmos_client):
        """Test creating a customer"""
        mock_client_instance = Mock()
        mock_database = Mock()
        mock_container = Mock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        # Mock the create_item response
        test_id = str(uuid.uuid4())
        mock_container.create_item.return_value = {
            "id": test_id,
            "firstname": "John",
            "lastname": "Doe",
            "age": 30
        }
        
        cosmos_client = CosmosDBClient()
        customer_data = CustomerCreate(firstname="John", lastname="Doe", age=30)
        
        result = await cosmos_client.create_customer(customer_data)
        
        assert isinstance(result, Customer)
        assert result.firstname == "John"
        assert result.lastname == "Doe"
        assert result.age == 30
        assert result.id == test_id
        mock_container.create_item.assert_called_once()
    
    @patch.dict(os.environ, {
        "COSMOS_URL": "https://test.documents.azure.com:443/",
        "COSMOS_CONNECTION_STRING": "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test==;",
        "COSMOS_DATABASE": "test_db",
        "COSMOS_CONTAINER": "test_container"
    })
    @patch('db.CosmosClient')
    @pytest.mark.asyncio
    async def test_get_customer_found(self, mock_cosmos_client):
        """Test getting an existing customer"""
        mock_client_instance = Mock()
        mock_database = Mock()
        mock_container = Mock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        test_id = "test-id-123"
        mock_container.read_item.return_value = {
            "id": test_id,
            "firstname": "John",
            "lastname": "Doe",
            "age": 30
        }
        
        cosmos_client = CosmosDBClient()
        result = await cosmos_client.get_customer(test_id)
        
        assert isinstance(result, Customer)
        assert result.id == test_id
        assert result.firstname == "John"
        mock_container.read_item.assert_called_once_with(item=test_id, partition_key=test_id)
    
    @patch.dict(os.environ, {
        "COSMOS_URL": "https://test.documents.azure.com:443/",
        "COSMOS_CONNECTION_STRING": "AccountEndpoint=https://test.documents.azure.com:443/;AccountKey=test==;",
        "COSMOS_DATABASE": "test_db",
        "COSMOS_CONTAINER": "test_container"
    })
    @patch('db.CosmosClient')
    @pytest.mark.asyncio
    async def test_get_customer_not_found(self, mock_cosmos_client):
        """Test getting a non-existent customer"""
        mock_client_instance = Mock()
        mock_database = Mock()
        mock_container = Mock()
        
        mock_cosmos_client.from_connection_string.return_value = mock_client_instance
        mock_client_instance.get_database_client.return_value = mock_database
        mock_database.get_container_client.return_value = mock_container
        
        mock_container.read_item.side_effect = CosmosResourceNotFoundError(404, "Not found")
        
        cosmos_client = CosmosDBClient()
        result = await cosmos_client.get_customer("non-existent-id")
        
        assert result is None


class TestFastAPIEndpoints:
    """Test FastAPI endpoints"""
    
    def test_root_endpoint(self):
        """Test root health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Customer Management API is running"}
    
    @patch('main.get_cosmos_client')
    def test_list_customers_empty(self, mock_get_cosmos_client):
        """Test listing customers when database is empty"""
        mock_cosmos_client = MagicMock()
        mock_cosmos_client.get_all_customers.return_value = []
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        response = client.get("/customers")
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('main.get_cosmos_client')
    def test_list_customers_with_data(self, mock_get_cosmos_client):
        """Test listing customers with data"""
        mock_cosmos_client = MagicMock()
        test_customers = [
            Customer(id="1", firstname="John", lastname="Doe", age=30),
            Customer(id="2", firstname="Jane", lastname="Smith", age=25)
        ]
        mock_cosmos_client.get_all_customers.return_value = test_customers
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        response = client.get("/customers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["firstname"] == "John"
        assert data[1]["firstname"] == "Jane"
    
    @patch('main.get_cosmos_client')
    def test_get_customer_found(self, mock_get_cosmos_client):
        """Test getting an existing customer"""
        mock_cosmos_client = MagicMock()
        test_customer = Customer(id="test-id", firstname="John", lastname="Doe", age=30)
        mock_cosmos_client.get_customer.return_value = test_customer
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        response = client.get("/customers/test-id")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-id"
        assert data["firstname"] == "John"
    
    @patch('main.get_cosmos_client')
    def test_get_customer_not_found(self, mock_get_cosmos_client):
        """Test getting a non-existent customer"""
        mock_cosmos_client = MagicMock()
        mock_cosmos_client.get_customer.return_value = None
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        response = client.get("/customers/non-existent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @patch('main.get_cosmos_client')
    def test_create_customer_success(self, mock_get_cosmos_client):
        """Test creating a customer successfully"""
        mock_cosmos_client = MagicMock()
        test_customer = Customer(id="new-id", firstname="John", lastname="Doe", age=30)
        mock_cosmos_client.create_customer.return_value = test_customer
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        customer_data = {
            "firstname": "John",
            "lastname": "Doe",
            "age": 30
        }
        
        response = client.post("/customers", json=customer_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "new-id"
        assert data["firstname"] == "John"
    
    def test_create_customer_invalid_data(self):
        """Test creating a customer with invalid data"""
        invalid_data = {
            "firstname": "",
            "lastname": "Doe",
            "age": 30
        }
        
        response = client.post("/customers", json=invalid_data)
        assert response.status_code == 422
    
    @patch('main.get_cosmos_client')
    def test_update_customer_success(self, mock_get_cosmos_client):
        """Test updating a customer successfully"""
        mock_cosmos_client = MagicMock()
        updated_customer = Customer(id="test-id", firstname="Jane", lastname="Doe", age=30)
        mock_cosmos_client.update_customer.return_value = updated_customer
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        update_data = {"firstname": "Jane"}
        
        response = client.put("/customers/test-id", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["firstname"] == "Jane"
    
    @patch('main.get_cosmos_client')
    def test_update_customer_not_found(self, mock_get_cosmos_client):
        """Test updating a non-existent customer"""
        mock_cosmos_client = MagicMock()
        mock_cosmos_client.update_customer.return_value = None
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        update_data = {"firstname": "Jane"}
        
        response = client.put("/customers/non-existent", json=update_data)
        assert response.status_code == 404
    
    @patch('main.get_cosmos_client')
    def test_delete_customer_success(self, mock_get_cosmos_client):
        """Test deleting a customer successfully"""
        mock_cosmos_client = MagicMock()
        mock_cosmos_client.delete_customer.return_value = True
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        response = client.delete("/customers/test-id")
        assert response.status_code == 204
    
    @patch('main.get_cosmos_client')
    def test_delete_customer_not_found(self, mock_get_cosmos_client):
        """Test deleting a non-existent customer"""
        mock_cosmos_client = MagicMock()
        mock_cosmos_client.delete_customer.return_value = False
        mock_get_cosmos_client.return_value = mock_cosmos_client
        
        response = client.delete("/customers/non-existent")
        assert response.status_code == 404
    
    @patch('main.get_cosmos_client')
    def test_cosmos_client_error_handling(self, mock_get_cosmos_client):
        """Test error handling when Cosmos DB client fails"""
        mock_get_cosmos_client.side_effect = ValueError("Missing required environment variables")
        
        response = client.get("/customers")
        assert response.status_code == 500  # Internal server error, not bad request
