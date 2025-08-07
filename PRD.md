## Project Requirements

Create a REST API using Pydantic, FastAPI and Azure Cosmos DB.

This REST endpoint will support CRUD operations to list, create, retrieve, update and delete customer records with the following data structure example:

````json
{
    "id": "e53f674e-89b8-459a-b16b-9e8d7987d5d8",
    "firstname": "Israel",
    "lastname" : "Ekpo",
    "email" : "israel@example.ai"
}
````

- add the necessary Python dependencies using uv
- add REST endpoint to list all records for customers
- add REST endpoint to retrieve specific customer by `id`
- add REST endpoint to create a customer record
- add REST endpoint to update customer record by `id`
- add REST endpoint to delete customer record by `id`

Cosmos DB endpoint will be retrieve from environment variable `COSMOS_URL`

Cosmos DB connection string will be retrieved from environment variable `COSMOS_CONNECTION_STRING`

The Cosmos DB database and container/collection will be retrieved from the environment variables `COSMOS_DATABASE` and `COSMOS_CONTAINER` respectively.

We are using `pydantic` version 2.11.7, `fastapi` version 0.116.1 and `azure-cosmos` 4.9.0