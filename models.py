from typing import Optional
from pydantic import BaseModel, Field
import uuid


class CustomerBase(BaseModel):
    firstname: str = Field(min_length=1, max_length=100)
    lastname: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=130)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    firstname: Optional[str] = Field(default=None, min_length=1, max_length=100)
    lastname: Optional[str] = Field(default=None, min_length=1, max_length=100)
    age: Optional[int] = Field(default=None, ge=0, le=130)


class Customer(CustomerBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": str(uuid.uuid4()),
                "firstname": "Israel",
                "lastname": "Ekpo",
                "age": 35,
            }
        }
    }


def apply_update(existing: Customer, update: CustomerUpdate) -> Customer:
    data = existing.model_dump()
    for field, value in update.model_dump(exclude_unset=True).items():
        data[field] = value
    return Customer(**data)
