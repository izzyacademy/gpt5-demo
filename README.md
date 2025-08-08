# Customer Management REST API

A FastAPI-based REST API for managing customer records with Azure Cosmos DB integration. This application provides full CRUD operations for customer data with automatic validation and error handling.

## How to Test
The generated application uses the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension by Huachao Mao.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete customer records
- **Data Validation**: Comprehensive input validation using Pydantic models
- **Azure Cosmos DB Integration**: Seamless integration with Azure Cosmos DB for data persistence
- **Auto-generated Documentation**: Interactive API documentation via FastAPI
- **Comprehensive Testing**: Full test suite with mocked dependencies
- **Error Handling**: Proper HTTP status codes and error messages

## Customer Data Model

```json
{
    "id": "e53f674e-89b8-459a-b16b-9e8d7987d5d8",
    "firstname": "Israel",
    "lastname": "Ekpo",
    "age": 35
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check endpoint |
| GET | `/customers` | List all customers |
| GET | `/customers/{id}` | Get customer by ID |
| POST | `/customers` | Create a new customer |
| PUT | `/customers/{id}` | Update customer by ID |
| DELETE | `/customers/{id}` | Delete customer by ID |

## Prerequisites

- Python 3.13 or higher
- Azure Cosmos DB account
- uv package manager (for dependency management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gpt5-demo
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables (copy from `.env.example`):
```bash
cp .env.example .env
# Edit .env with your actual Azure Cosmos DB configuration
```

## Environment Variables

Create a `.env` file with the following variables:

```env
COSMOS_URL=https://your-cosmosdb-account.documents.azure.com:443/
COSMOS_CONNECTION_STRING=AccountEndpoint=https://your-cosmosdb-account.documents.azure.com:443/;AccountKey=your-primary-key;
COSMOS_DATABASE=customers-db
COSMOS_CONTAINER=customers
```

## Running the Application

### Development Server

```bash
# Using uv
uv run main.py

# Or using Python directly
python main.py
```

The API will be available at `http://localhost:8000`

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage Examples

### Create a Customer
```bash
curl -X POST "http://localhost:8000/customers" \
     -H "Content-Type: application/json" \
     -d '{
       "firstname": "John",
       "lastname": "Doe",
       "age": 30
     }'
```

### Get All Customers
```bash
curl -X GET "http://localhost:8000/customers"
```

### Get Customer by ID
```bash
curl -X GET "http://localhost:8000/customers/{customer-id}"
```

### Update a Customer
```bash
curl -X PUT "http://localhost:8000/customers/{customer-id}" \
     -H "Content-Type: application/json" \
     -d '{
       "firstname": "Jane",
       "age": 31
     }'
```

### Delete a Customer
```bash
curl -X DELETE "http://localhost:8000/customers/{customer-id}"
```

## Testing

Run the test suite:

```bash
# Run all tests
uv run pytest test_main.py -v

# Run specific test class
uv run pytest test_main.py::TestCustomerAPI -v

# Run with coverage
uv run pytest test_main.py --cov=. --cov-report=html
```

## Project Structure

```
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic data models
├── db.py               # Azure Cosmos DB client and operations
├── test_main.py        # Test suite
├── .env.example        # Environment variables template
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock            # Dependency lock file
└── README.md          # This file
```

## Dependencies

- **FastAPI** (0.116.1): Modern web framework for building APIs
- **Pydantic** (2.11.7): Data validation using Python type annotations
- **Azure Cosmos** (4.9.0): Azure Cosmos DB SDK for Python
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pytest**: Testing framework
- **httpx**: HTTP client for testing

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Customer not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
