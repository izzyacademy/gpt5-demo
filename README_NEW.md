# Customer Management API

A REST API built with FastAPI, Pydantic, and Azure Cosmos DB for managing customer records.

## Features

- **CRUD Operations**: Create, Read, Update, Delete customer records
- **Data Validation**: Comprehensive input validation using Pydantic
- **Azure Cosmos DB Integration**: Scalable NoSQL database backend
- **OpenAPI Documentation**: Auto-generated interactive API docs
- **Comprehensive Testing**: Unit tests with pytest and mocking
- **Error Handling**: Robust error handling and HTTP status codes

## Customer Data Structure

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
| `GET` | `/` | Health check endpoint |
| `GET` | `/customers` | List all customers |
| `GET` | `/customers/{id}` | Get customer by ID |
| `POST` | `/customers` | Create new customer |
| `PUT` | `/customers/{id}` | Update customer by ID |
| `DELETE` | `/customers/{id}` | Delete customer by ID |

## Requirements

- Python 3.13+
- Azure Cosmos DB account
- Required dependencies (see `pyproject.toml`)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd gpt5-demo
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Copy `.env.example` to `.env` and configure your Azure Cosmos DB settings:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your Azure Cosmos DB credentials:
   ```env
   COSMOS_URL=https://your-cosmos-account.documents.azure.com:443/
   COSMOS_CONNECTION_STRING=AccountEndpoint=https://your-cosmos-account.documents.azure.com:443/;AccountKey=your-account-key==;
   COSMOS_DATABASE=customer_db
   COSMOS_CONTAINER=customers
   ```

## Usage

### Running the Server

**Option 1: Using the main script**:
```bash
python main.py
```

**Option 2: Using uvicorn directly**:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

Visit `http://localhost:8000/docs` for auto-generated interactive API documentation.

### Example API Usage

**Create a customer**:
```bash
curl -X POST "http://localhost:8000/customers" \
     -H "Content-Type: application/json" \
     -d '{
       "firstname": "John",
       "lastname": "Doe", 
       "age": 30
     }'
```

**Get all customers**:
```bash
curl -X GET "http://localhost:8000/customers"
```

**Get customer by ID**:
```bash
curl -X GET "http://localhost:8000/customers/{customer_id}"
```

**Update a customer**:
```bash
curl -X PUT "http://localhost:8000/customers/{customer_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "firstname": "Jane"
     }'
```

**Delete a customer**:
```bash
curl -X DELETE "http://localhost:8000/customers/{customer_id}"
```

## Testing

Run the test suite:
```bash
pytest test_main.py -v
```

Run tests with async support:
```bash
pytest test_main.py -v --asyncio-mode=auto
```

Run the demo script:
```bash
python demo.py
```

## Project Structure

```
gpt5-demo/
├── main.py              # FastAPI application and routes
├── models.py            # Pydantic data models
├── db.py                # Azure Cosmos DB client and operations
├── test_main.py         # Comprehensive test suite
├── demo.py              # Demonstration script
├── .env.example         # Example environment variables
├── pyproject.toml       # Project dependencies and configuration
├── README.md            # This file
├── PRD.md               # Product Requirements Document
└── validation.http      # HTTP request examples
```

## Dependencies

- **FastAPI 0.116.1**: Modern web framework for building APIs
- **Pydantic 2.11.7**: Data validation and settings management
- **Azure Cosmos 4.9.0**: Azure Cosmos DB client
- **Uvicorn**: ASGI server for running the application
- **Pytest**: Testing framework with async support
- **HTTPx**: HTTP client for testing
- **Python-dotenv**: Environment variable management

## Validation Rules

- **firstname**: Required, 1-100 characters
- **lastname**: Required, 1-100 characters  
- **age**: Required, integer between 0 and 150
- **id**: Auto-generated UUID for new customers

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Customer not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

## Azure Cosmos DB Setup

1. Create an Azure Cosmos DB account
2. Create a database (e.g., `customer_db`)
3. Create a container (e.g., `customers`) with partition key `/id`
4. Configure the environment variables with your connection details

## Development

### Adding New Features

1. Update `models.py` for new data structures
2. Add database operations in `db.py`
3. Create new endpoints in `main.py`
4. Add tests in `test_main.py`

### Code Quality

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for all public methods
- Write comprehensive tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request
