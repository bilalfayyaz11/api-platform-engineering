# JWT Authentication API

## What This Does

This implementation provides a token-based authentication service built with Node.js and Express.

Users can register with a username and password, authenticate with their credentials, receive a signed JSON Web Token, and use that token to access protected API endpoints.

Passwords are hashed with bcryptjs before storage. Authentication tokens include expiration, issuer, audience, issued-at, and authenticated-user claims. Express middleware validates each token before allowing access to protected resources.

The implementation also handles missing tokens, malformed authorization headers, invalid signatures, expired tokens, duplicate usernames, invalid credentials, malformed JSON, and unknown endpoints.

## Architecture

    Client
      |
      | POST /api/auth/register
      | POST /api/auth/login
      v
    Express Authentication Routes
      |
      |-- Validate request data
      |-- Hash and compare passwords
      |-- Generate signed JWT
      v
    In-Memory User Store

    Client
      |
      | Authorization: Bearer <JWT>
      v
    JWT Verification Middleware
      |
      |-- Extract Bearer token
      |-- Validate signature
      |-- Validate issuer and audience
      |-- Validate expiration
      |-- Attach decoded identity to req.user
      v
    Protected API Routes
      |
      |-- GET /api/dashboard
      |-- GET /api/profile
      v
    Authenticated JSON Response

## API Endpoints

### Service Health

    GET /

Confirms that the authentication service is running.

### Register User

    POST /api/auth/register

Example request:

    {
      "username": "alice",
      "password": "secure123"
    }

The password is hashed with bcryptjs before being stored.

### Login

    POST /api/auth/login

Example request:

    {
      "username": "alice",
      "password": "secure123"
    }

A successful login returns a signed JWT:

    {
      "message": "Login successful",
      "token": "<signed-token>",
      "tokenType": "Bearer",
      "expiresIn": "1h"
    }

### Public Endpoint

    GET /api/public

This endpoint does not require authentication.

### Protected Dashboard

    GET /api/dashboard

Required header:

    Authorization: Bearer <token>

### Protected Profile

    GET /api/profile

Required header:

    Authorization: Bearer <token>

## Security Controls

The service includes the following controls:

- Password hashing with bcryptjs and ten salt rounds
- Cryptographically generated JWT signing secret
- Environment-based secret management
- JWT expiration validation
- JWT issuer and audience validation
- Bearer authorization scheme enforcement
- Generic invalid-credential responses
- Duplicate-user protection
- Request-body validation
- JSON body-size restriction
- Malformed JSON handling
- Protected-route middleware
- Sensitive file exclusion through `.gitignore`

The `.env` file, generated tokens, process files, logs, and dependency directories are excluded from version control.

## HTTP Status Handling

The API uses meaningful status codes:

    200  Successful request
    201  User created successfully
    400  Invalid input or malformed JSON
    401  Invalid credentials, invalid token, or expired token
    403  Missing token or incorrect authorization format
    404  Endpoint not found
    409  Username already exists
    500  Internal server error

## Technology Stack

- Node.js
- Express.js
- JSON Web Token
- bcryptjs
- dotenv
- Nodemon
- curl
- Linux

## File Structure

    jwt-auth-lab/
    ├── middleware/
    │   └── authMiddleware.js
    ├── routes/
    │   ├── auth.js
    │   └── protected.js
    ├── .env
    ├── .gitignore
    ├── package-lock.json
    ├── package.json
    ├── server.js
    └── test-auth.sh

The `.env` file is required locally but must never be committed.

## Setup

Clone the repository:

    git clone https://github.com/bilalfayyaz11/api-platform-engineering.git
    cd api-platform-engineering

Install dependencies:

    npm install

Generate a secure JWT secret:

    openssl rand -hex 64

Create the environment file:

    cat > .env << 'ENVEOF'
    PORT=3000
    JWT_SECRET=replace_with_a_secure_random_secret
    JWT_EXPIRES_IN=1h
    ENVEOF

Protect the environment file:

    chmod 600 .env

Start the service:

    npm start

For development with automatic restart:

    npm run dev

## Reproduce the Authentication Flow

Register a user:

    curl -X POST http://localhost:3000/api/auth/register \
      -H "Content-Type: application/json" \
      -d '{"username":"alice","password":"secure123"}'

Log in:

    curl -X POST http://localhost:3000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"username":"alice","password":"secure123"}'

Copy the returned token and access the dashboard:

    curl http://localhost:3000/api/dashboard \
      -H "Authorization: Bearer YOUR_TOKEN"

Access the authenticated profile:

    curl http://localhost:3000/api/profile \
      -H "Authorization: Bearer YOUR_TOKEN"

Test access without a token:

    curl http://localhost:3000/api/dashboard

Test an invalid token:

    curl http://localhost:3000/api/dashboard \
      -H "Authorization: Bearer invalid.token.here"

## Token Expiration Verification

Temporarily configure a short expiration:

    JWT_EXPIRES_IN=10s

Restart the service, register and authenticate again, then access a protected endpoint immediately.

After waiting longer than ten seconds, submit the same token again. The service should return HTTP 401 with an expiration message.

Restore the normal setting afterward:

    JWT_EXPIRES_IN=1h

## Validation

Check JavaScript syntax:

    node --check server.js
    node --check routes/auth.js
    node --check routes/protected.js
    node --check middleware/authMiddleware.js

Review installed dependencies:

    npm list --depth=0

Verify the listening port:

    sudo lsof -i :3000

## Real-World Use Case

This authentication pattern can protect:

- AI inference APIs
- Internal automation services
- Microservice endpoints
- Administrative dashboards
- Data-processing APIs
- Platform engineering services
- Machine-learning operations interfaces

A client authenticates once, receives a signed token, and presents that token when requesting protected resources. The backend verifies the token without maintaining a traditional server-side session.

## Current Limitations

User records are stored in memory. They disappear whenever the Node.js process restarts.

A production version should add:

- PostgreSQL or another persistent database
- Refresh-token rotation
- Token revocation or denylisting
- Login rate limiting
- Account lockout controls
- Password-reset workflows
- Role-based access control
- Audit logging
- HTTPS termination
- Centralised secret management

## Skills Demonstrated

- REST API development
- JWT generation and verification
- Password hashing
- Express middleware design
- Authentication and authorization
- Environment-secret management
- HTTP status-code handling
- Input validation
- API security testing
- Linux service troubleshooting
- Node.js dependency management

## Lessons Learned

JWT decoding and JWT verification are different operations. Anyone can decode an ordinary JWT payload, but only a service with the correct signing secret can verify that the token is authentic.

Passwords must never be stored in plaintext. They should be processed using an established password-hashing algorithm before storage.

Authentication middleware provides a reusable security boundary. Protected endpoints do not need to implement token validation independently because requests must pass through middleware first.

Environment secrets must remain outside version control. Accidentally committing a signing secret can allow attackers to generate trusted tokens.

Token expiration limits the useful lifetime of a stolen credential, but production systems also require refresh-token controls and revocation capabilities.

## Troubleshooting

### Node.js Module Not Found

Install dependencies:

    npm install

### Port 3000 Already in Use

Identify the process:

    sudo lsof -i :3000

Stop it:

    kill <PROCESS_ID>

### JWT Verification Fails

Confirm that token generation and verification use the same `JWT_SECRET`.

Verify the header format:

    Authorization: Bearer <token>

Confirm that issuer and audience values match the values configured during token generation.

### Registered User Disappears

The current implementation stores users in memory. Restarting the Node.js process clears all registered users.

Register the user again or replace the in-memory array with persistent database storage.

### Token Immediately Appears Expired

Check the configured expiration:

    grep '^JWT_EXPIRES_IN=' .env

Restore the normal value:

    JWT_EXPIRES_IN=1h
