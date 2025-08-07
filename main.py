import os
from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from models import Customer, CustomerCreate, CustomerUpdate, CustomerResponse
from db import get_cosmos_client


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Customer Management API",
    description="A REST API for managing customer records with Azure Cosmos DB",
    version="1.0.0",
)


@app.get("/", summary="Health Check")
async def root():
    """Health check endpoint"""
    return {"message": "Customer Management API is running"}


@app.get("/customers", response_model=List[CustomerResponse], summary="List all customers")
async def list_customers():
    """
    Get all customer records
    
    Returns:
        List[CustomerResponse]: List of all customers
    """
    try:
        cosmos_client = get_cosmos_client()
        customers = await cosmos_client.get_all_customers()
        return customers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve customers: {str(e)}"
        )


@app.get("/customers/{customer_id}", response_model=CustomerResponse, summary="Get customer by ID")
async def get_customer(customer_id: str):
    """
    Get a specific customer by ID
    
    Args:
        customer_id (str): The unique customer identifier
        
    Returns:
        CustomerResponse: The customer data
        
    Raises:
        HTTPException: 404 if customer not found
    """
    try:
        cosmos_client = get_cosmos_client()
        customer = await cosmos_client.get_customer(customer_id)
        
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found"
            )
        
        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve customer: {str(e)}"
        )


@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, summary="Create a new customer")
async def create_customer(customer_data: CustomerCreate):
    """
    Create a new customer record
    
    Args:
        customer_data (CustomerCreate): The customer data to create
        
    Returns:
        CustomerResponse: The created customer with generated ID
    """
    try:
        cosmos_client = get_cosmos_client()
        new_customer = await cosmos_client.create_customer(customer_data)
        return new_customer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create customer: {str(e)}"
        )


@app.put("/customers/{customer_id}", response_model=CustomerResponse, summary="Update customer by ID")
async def update_customer(customer_id: str, customer_update: CustomerUpdate):
    """
    Update a specific customer by ID
    
    Args:
        customer_id (str): The unique customer identifier
        customer_update (CustomerUpdate): The customer data to update
        
    Returns:
        CustomerResponse: The updated customer data
        
    Raises:
        HTTPException: 404 if customer not found
    """
    try:
        cosmos_client = get_cosmos_client()
        updated_customer = await cosmos_client.update_customer(customer_id, customer_update)
        
        if updated_customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found"
            )
        
        return updated_customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update customer: {str(e)}"
        )


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete customer by ID")
async def delete_customer(customer_id: str):
    """
    Delete a specific customer by ID
    
    Args:
        customer_id (str): The unique customer identifier
        
    Raises:
        HTTPException: 404 if customer not found
    """
    try:
        cosmos_client = get_cosmos_client()
        deleted = await cosmos_client.delete_customer(customer_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete customer: {str(e)}"
        )


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


# For running the application
def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
