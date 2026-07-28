# API Versioning Service

## Overview

This Flask service demonstrates how REST APIs can evolve without breaking existing clients.

It runs two API versions simultaneously:

- `v1` preserves the original response contract.
- `v2` adds metadata, structured errors, and user creation.
- `v1` includes deprecation and sunset headers to guide client migration.

## Architecture

```text
                     Client Applications
                             |
              +--------------+--------------+
              |                             |
              v                             v
        /api/v1/users                 /api/v2/users
        /api/v1/users/{id}            /api/v2/users/{id}
                                      POST /api/v2/users
              |                             |
              +--------------+--------------+
                             |
                             v
                     Flask Application
                             |
              +--------------+--------------+
              |                             |
              v                             v
          V1 Formatter                  V2 Formatter
        id, name, email          id, name, email,
                                 created_at, version
              |                             |
              +--------------+--------------+
                             |
                             v
                    In-Memory User Store
                             |
                             v
                   Versioning Utilities
            API-Version, Deprecation,
                 Sunset and Warning
```

## Features

- URL path versioning
- Parallel `v1` and `v2` support
- Backward-compatible response contracts
- Version-specific business logic
- Deprecation and sunset headers
- Structured error responses
- JSON request validation
- Duplicate-email protection
- UTC creation timestamps
- Correct HTTP status codes

## Technology Stack

- Python 3.12
- Flask
- Requests
- REST
- JSON
- Linux
- curl
- Git

## Directory Structure

```text
api-versioning-service/
├── app.py
├── versioning_utils.py
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service health |
| GET | `/api/v1/users` | List users using the v1 contract |
| GET | `/api/v1/users/{id}` | Retrieve one v1 user |
| GET | `/api/v2/users` | List users with metadata |
| GET | `/api/v2/users/{id}` | Retrieve one v2 user |
| POST | `/api/v2/users` | Create a user |

## Response Contracts

### Version 1

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

### Version 2

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "created_at": "2026-01-15T10:30:00+00:00",
  "version": "v2"
}
```

## Deprecation Headers

Version 1 responses include:

```text
API-Version: v1
Deprecation: true
Sunset: Fri, 31 Dec 2027 23:59:59 GMT
Warning: 299 - "API v1 is deprecated; migrate to API v2"
```

## Setup

```bash
git clone https://github.com/bilalfayyaz11/api-platform-engineering.git
cd api-platform-engineering/api-versioning-service

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

The service runs at:

```text
http://localhost:5000
```

## Test Version 1

```bash
curl -i http://localhost:5000/api/v1/users
curl -i http://localhost:5000/api/v1/users/1
```

Version 1 returns only:

- `id`
- `name`
- `email`

It also returns API lifecycle headers.

## Test Version 2

```bash
curl -i http://localhost:5000/api/v2/users
curl -i http://localhost:5000/api/v2/users/1
```

Version 2 additionally returns:

- `created_at`
- `version`

## Create a User

```bash
curl -i \
  -X POST \
  http://localhost:5000/api/v2/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Charlie Brown","email":"charlie@example.com"}'
```

Expected status:

```text
HTTP/1.1 201 CREATED
Location: /api/v2/users/3
```

## Test Error Handling

Missing user:

```bash
curl -i http://localhost:5000/api/v2/users/999
```

Missing required field:

```bash
curl -i \
  -X POST \
  http://localhost:5000/api/v2/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Incomplete User"}'
```

Duplicate email:

```bash
curl -i \
  -X POST \
  http://localhost:5000/api/v2/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Duplicate User","email":"alice@example.com"}'
```

Expected status codes:

```text
404 Not Found
400 Bad Request
409 Conflict
```

## Verification

Check Python syntax:

```bash
python -m py_compile app.py versioning_utils.py
```

Check both API versions:

```bash
v1_status=$(curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:5000/api/v1/users)

v2_status=$(curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:5000/api/v2/users)

[ "$v1_status" = "200" ] && echo "V1 operational"
[ "$v2_status" = "200" ] && echo "V2 operational"
```

Check deprecation headers:

```bash
curl -i -s http://localhost:5000/api/v1/users \
  | grep -Ei "API-Version|Deprecation|Sunset|Warning"
```

## Design Decisions

### Stable Version Contracts

Separate formatter functions control which fields each API version exposes. Internal data changes therefore do not automatically break older clients.

### Persistent Creation Timestamps

Creation timestamps are stored with user records rather than regenerated during every GET request.

### UTC Timestamps

New users receive timezone-aware UTC timestamps:

```python
datetime.now(timezone.utc).isoformat()
```

### Isolated Version Behaviour

User creation and enhanced errors are available only in `v2`. Version 1 remains compatible with existing consumers.

### Reusable Utilities

Version headers, deprecation behaviour, and version detection are implemented in `versioning_utils.py`.

## Skills Demonstrated

- REST API design
- Flask development
- API versioning
- Backward compatibility
- API contract management
- HTTP lifecycle headers
- JSON validation
- Structured errors
- HTTP status codes
- Linux API testing
- Git source control

## Limitations

The service uses an in-memory data store. Created users are removed when the application restarts.

A production implementation should add:

- PostgreSQL persistence
- Authentication and authorisation
- Automated tests
- OpenAPI documentation
- Rate limiting
- Structured logging
- Containerisation
- Monitoring and tracing

## Outcome

This implementation demonstrates how an API can introduce new functionality while preserving existing client integrations.

It covers version-specific contracts, backward compatibility, deprecation communication, validation, error handling, and controlled API evolution.
