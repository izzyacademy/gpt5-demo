#!/usr/bin/env python3
"""
Simple demonstration script for the Customer Management API
"""
import asyncio
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set up test environment variables
import os
os.environ["COSMOS_URL"] = "https://test-cosmos.documents.azure.com:443/"
os.environ["COSMOS_CONNECTION_STRING"] = "AccountEndpoint=https://test-cosmos.documents.azure.com:443/;AccountKey=test-key==;"
os.environ["COSMOS_DATABASE"] = "test_customer_db"
os.environ["COSMOS_CONTAINER"] = "test_customers"

from main import app
from models import Customer, CustomerCreate

def demo_api():
    """Demonstrate the API functionality with mock data"""
    print("🚀 Customer Management API Demo")
    print("=" * 50)
    
    with TestClient(app) as client:
        # Test 1: Health check
        print("\n1. Testing health check endpoint...")
        response = client.get("/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test 2: Input validation
        print("\n2. Testing input validation...")
        invalid_customer = {
            "firstname": "",  # Invalid: empty string
            "lastname": "Doe",
            "age": 30
        }
        response = client.post("/customers", json=invalid_customer)
        print(f"   Status: {response.status_code} (Expected: 422 for validation error)")
        
        # Test 3: Valid customer data structure
        print("\n3. Testing valid customer data structure...")
        valid_customer = CustomerCreate(
            firstname="John", 
            lastname="Doe", 
            age=30
        )
        print(f"   Valid customer model: {valid_customer.model_dump()}")
        
        # Test 4: Customer model with ID
        print("\n4. Testing complete customer model...")
        complete_customer = Customer(
            id="e53f674e-89b8-459a-b16b-9e8d7987d5d8",
            firstname="Israel",
            lastname="Ekpo",
            age=35
        )
        print(f"   Complete customer: {complete_customer.model_dump()}")
        print(f"   JSON representation:")
        print(f"   {json.dumps(complete_customer.model_dump(), indent=2)}")


def demo_models():
    """Demonstrate the Pydantic models"""
    print("\n📋 Pydantic Models Demo")
    print("=" * 30)
    
    # Test CustomerCreate
    print("\n✅ CustomerCreate model:")
    customer_create = CustomerCreate(
        firstname="Alice",
        lastname="Johnson", 
        age=28
    )
    print(f"   {customer_create.model_dump()}")
    
    # Test validation
    print("\n❌ Testing validation (this should fail):")
    try:
        invalid_customer = CustomerCreate(
            firstname="",  # Empty string should fail
            lastname="Smith",
            age=25
        )
    except ValueError as e:
        print(f"   Validation error (expected): {e}")
    
    # Test age validation
    try:
        invalid_age = CustomerCreate(
            firstname="Bob",
            lastname="Wilson",
            age=-5  # Negative age should fail
        )
    except ValueError as e:
        print(f"   Age validation error (expected): {e}")


if __name__ == "__main__":
    try:
        demo_models()
        demo_api()
        
        print("\n🎉 Demo completed successfully!")
        print("\n📚 API Endpoints Available:")
        print("   GET    /                     - Health check")
        print("   GET    /customers            - List all customers") 
        print("   GET    /customers/{id}       - Get customer by ID")
        print("   POST   /customers            - Create new customer")
        print("   PUT    /customers/{id}       - Update customer")
        print("   DELETE /customers/{id}       - Delete customer")
        
        print("\n🔧 To run the server:")
        print("   python main.py")
        print("   # or")
        print("   uvicorn main:app --reload")
        
        print("\n📖 OpenAPI docs available at:")
        print("   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
