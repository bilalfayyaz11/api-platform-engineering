# Swagger OpenAPI Service

## Overview

This implementation demonstrates how to build a production-style REST API with automatic OpenAPI 3.0 documentation using Flask-RESTX.

The service provides interactive Swagger UI, request validation, documented response models, filtering, and CRUD operations for a simple book library.

## Architecture

```text
                     Client / Browser
                            |
          +-----------------+-----------------+
          |                                   |
          v                                   v
      REST API                        Swagger UI (/docs)
          |                                   |
          +-----------------+-----------------+
                            |
                     Flask-RESTX API
                            |
          +-----------------+-----------------+
          |                                   |
          v                                   v
     API Resources                    OpenAPI Generator
          |                                   |
          +-----------------+-----------------+
                            |
                            v
                     In-Memory Book Store
```

## Features

- OpenAPI 3.0 specification
- Automatic Swagger UI generation
- Interactive API testing
- CRUD operations
- Request validation
- Response schemas
- Query parameter filtering
- Documented HTTP responses
- JSON API
- Automatic OpenAPI JSON export

## Technology Stack

- Python 3.12
- Flask
- Flask-RESTX
- OpenAPI 3.0
- Swagger UI
- REST API
- JSON
- Linux
- curl
- Git

## Directory Structure

```text
swagger-openapi-service/
├── app.py
├── openapi_spec.json
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Service health |
| GET | `/books/` | List all books |
| POST | `/books/` | Create a book |
| GET | `/books/{id}` | Retrieve a book |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |
| GET | `/docs` | Swagger UI |
| GET | `/swagger.json` | OpenAPI specification |

## Setup

```bash
git clone https://github.com/bilalfayyaz11/api-platform-engineering.git
cd api-platform-engineering/swagger-openapi-service

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```bash
source venv/bin/activate
python app.py
```

Application:

```text
http://localhost:5000
```

Swagger UI:

```text
http://localhost:5000/docs
```

OpenAPI Specification:

```text
http://localhost:5000/swagger.json
```

## Testing

List books:

```bash
curl http://localhost:5000/books/
```

Retrieve a book:

```bash
curl http://localhost:5000/books/1
```

Filter by author:

```bash
curl "http://localhost:5000/books/?author=Orwell"
```

Filter by year:

```bash
curl "http://localhost:5000/books/?year=1949"
```

Create a book:

```bash
curl -X POST http://localhost:5000/books/ \
-H "Content-Type: application/json" \
-d '{"title":"Brave New World","author":"Aldous Huxley","year":1932,"isbn":"9780060850524"}'
```

Update a book:

```bash
curl -X PUT http://localhost:5000/books/1 \
-H "Content-Type: application/json" \
-d '{"title":"1984 Updated","author":"George Orwell","year":1949,"isbn":"9780451524935"}'
```

Delete a book:

```bash
curl -X DELETE http://localhost:5000/books/2
```

## Verification

Verify Python syntax:

```bash
python -m py_compile app.py
```

Verify OpenAPI specification:

```bash
curl http://localhost:5000/swagger.json | python3 -m json.tool
```

Verify Swagger UI:

```bash
curl -I http://localhost:5000/docs
```

## Skills Demonstrated

- REST API Development
- Flask
- Flask-RESTX
- OpenAPI 3.0
- Swagger Documentation
- API Validation
- API Modelling
- CRUD Operations
- Query Parameter Filtering
- JSON Processing
- Linux Development
- Git

## Real-World Applications

- Public API documentation
- Internal developer portals
- Backend microservices
- API-first development
- Client SDK generation
- API testing and validation

## Future Enhancements

- PostgreSQL integration
- Authentication and authorization
- JWT security
- Pagination
- Sorting
- Rate limiting
- Docker deployment
- Automated testing
- CI/CD integration
- Monitoring and logging

## Outcome

This implementation demonstrates how to build well-documented REST APIs using Flask-RESTX and OpenAPI. It provides interactive Swagger documentation, request validation, response modelling, and API specification generation while following modern API development practices.
