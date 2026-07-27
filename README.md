# API Platform Engineering

## Overview

This repository contains backend API implementations focused on authentication, service security, middleware design, request validation, and platform-oriented API engineering.

Each implementation is organised in its own directory with independent source code, dependencies, setup instructions, verification steps, security considerations, and troubleshooting guidance.

## Implementations

### JWT Authentication Service

Location:

    jwt-authentication-service/

A Node.js and Express authentication service that provides:

- User registration
- bcrypt password hashing
- JWT token generation
- JWT signature and expiration validation
- Middleware-protected endpoints
- Public and authenticated routes
- Issuer and audience claim verification
- Missing, malformed, invalid, and expired token handling
- Input validation and meaningful HTTP responses

Documentation:

    jwt-authentication-service/README.md

## Repository Structure

    api-platform-engineering/
    ├── jwt-authentication-service/
    │   ├── middleware/
    │   │   └── authMiddleware.js
    │   ├── routes/
    │   │   ├── auth.js
    │   │   └── protected.js
    │   ├── .gitignore
    │   ├── package-lock.json
    │   ├── package.json
    │   ├── README.md
    │   ├── server.js
    │   └── test-auth.sh
    └── README.md

## Engineering Areas

The repository demonstrates practical experience in:

- REST API development
- Authentication and authorization
- API security
- Express middleware
- Token-based identity
- Password protection
- Environment-secret management
- HTTP status handling
- Backend testing
- Linux service operations
- Node.js dependency management

## Usage

Open the directory for the implementation you want to run and follow its README.

Example:

    cd jwt-authentication-service
    npm install

Create the required environment configuration and then start the service:

    npm start

## Security Notice

Environment files, credentials, tokens, process files, dependency directories, and application logs must not be committed.

Each implementation contains its own `.gitignore` and security guidance.
