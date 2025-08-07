from fastapi import FastAPI, HTTPException, Depends
from models import Customer, CustomerCreate, CustomerUpdate
from db import CustomerRepository

app = FastAPI(title="Customer API")


def get_repo():
    return CustomerRepository()


@app.get("/customers", response_model=list[Customer])
def list_customers(repo: CustomerRepository = Depends(get_repo)):
    return repo.list()


@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: str, repo: CustomerRepository = Depends(get_repo)):
    customer = repo.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.post("/customers", response_model=Customer, status_code=201)
def create_customer(payload: CustomerCreate, repo: CustomerRepository = Depends(get_repo)):
    return repo.create(payload)


@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: str, payload: CustomerUpdate, repo: CustomerRepository = Depends(get_repo)):
    updated = repo.update(customer_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: str, repo: CustomerRepository = Depends(get_repo)):
    ok = repo.delete(customer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None


# If executed directly, run uvicorn
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
