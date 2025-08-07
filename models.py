from pydantic import BaseModel, Field
from typing import Optional
import uuid


class CustomerBase(BaseModel):
    """Base customer model with common fields"""
    firstname: str = Field(..., min_length=1, max_length=100, description="Customer's first name")
    lastname: str = Field(..., min_length=1, max_length=100, description="Customer's last name")
    age: int = Field(..., ge=0, le=150, description="Customer's age")


class CustomerCreate(CustomerBase):
    """Model for creating a new customer"""
    pass


class CustomerUpdate(BaseModel):
    """Model for updating an existing customer"""
    firstname: Optional[str] = Field(None, min_length=1, max_length=100, description="Customer's first name")
    lastname: Optional[str] = Field(None, min_length=1, max_length=100, description="Customer's last name")
    age: Optional[int] = Field(None, ge=0, le=150, description="Customer's age")


class Customer(CustomerBase):
    """Complete customer model with ID"""
    id: str = Field(..., description="Unique customer identifier")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "e53f674e-89b8-459a-b16b-9e8d7987d5d8",
                "firstname": "Israel",
                "lastname": "Ekpo",
                "age": 35
            }
        }
    }


class CustomerResponse(Customer):
    """Customer response model"""
    pass


def generate_customer_id() -> str:
    """Generate a new UUID for customer ID"""
    return str(uuid.uuid4())
