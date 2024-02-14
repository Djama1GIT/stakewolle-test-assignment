# Stakewolle Test Assignment

Referral system

## Installation and Setup

1. Install Docker and Docker Compose if they are not already installed on your system.

2. Clone the project repository:

```bash
git clone https://github.com/Djama1GIT/stakewolle-test-assignment.git
cd stakewolle-test-assignment
```

3. Start the project:

```bash
docker-compose up --build
```

## User Interface

After starting the project, you can access the Swagger user interface at: http://localhost:8080/docs.<br>
In Swagger, you can view the available endpoints and their parameters, and also make requests to the API.

## Usage Examples

1. Login:

```bash
curl -i -X POST -d \
  "grant_type=password&username=user@example.com&password=string&scope=&client_id=&client_secret=" \
  http://localhost:8080/auth/login
```

```
HTTP/1.1 204 No Content
date: Tue, 13 Feb 2024 23:20:09 GMT
server: uvicorn
set-cookie: fastapiusersauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3MDc4NzAwMDl9.tt5DLy0MJOJWjgK4zsAfGIOkNlGQ3OjVuqyRkXltShQ; HttpOnly; Max-Age=3600; Path=/; SameSite=lax; Secure
```

2. Logout:

```bash
curl -i -X POST -H "Cookie: fastapiusersauth=your_jwt_token" \
http://localhost:8080/auth/logout
```

```
HTTP/1.1 204 No Content
date: Tue, 13 Feb 2024 23:21:42 GMT
server: uvicorn
set-cookie: fastapiusersauth=""; HttpOnly; Max-Age=0; Path=/; SameSite=lax; Secure
```

3. User registration:

```bash
curl -i -X POST -H "Content-Type: application/json" -d \
  '{
    "email": "user@example.com",
    "password": "string",
    "is_active": true,
    "is_superuser": false, 
    "is_verified": false
  }' http://localhost:8080/auth/register/
```

```
HTTP/1.1 200 OK
date: Tue, 13 Feb 2024 23:14:09 GMT
server: uvicorn
content-length: 199
content-type: application/json
```

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "referral_code": null,
  "referral_expiration": null,
  "referrer_id": null,
  "referrals": null,
  "referrer": null
}
```

4. Getting information about your referrals:

```bash
curl -X GET -H "Cookie: fastapiusersauth=your_jwt_token" \
  http://localhost:8080/referrals/my
```

```json
{
  "referrer": 1,
  "referrals": [
    115,
    116,
    117
  ]
}
```

5. Getting information about referrals by their ID:

```bash
curl -X GET http://localhost:8080/referrals/by_id/1
```

```json
{
  "referrer": 1,
  "referrals": [
    115,
    116,
    117
  ]
}
```

6. Getting the referrer code by email:

```bash
curl -X GET http://localhost:8080/referrals/code_by_email/user@example.com
```

```json
{
  "code": "GADJIIAVOV"
}
```

7. Getting information about referrals by email:

```bash
curl -X GET http://localhost:8080/referrals/by_email/user@example.com
```

```json
{
  "referrer": "user@example.com",
  "referrals": [
    115,
    116,
    117
  ]
}
```

8. Getting information about referrals by code:

```bash
curl -X GET http://localhost:8080/referrals/by_code/GADJIIAVOV
```

```json
{
  "referrer": "GADJIIAVOV",
  "referrals": [
    115,
    116,
    117
  ]
}
```

9. Creating a referrer code:

```bash
curl -X POST -H "Content-Type: application/json" \
  -H "Cookie: fastapiusersauth=your_jwt_token" \
  -d '{"code": "GADJIIAVOV", "expiration": 7}' \
  http://localhost:8080/referrals/create_code
```

```json
{
  "code": "GADJIIAVOV",
  "expiration": 7
}
```

10. Deleting a referrer code:

```bash
curl -i -X DELETE -H "Cookie: fastapiusersauth=your_jwt_token" \
  http://localhost:8080/referrals/delete_code
```

```
HTTP/1.1 200 OK
date: Tue, 13 Feb 2024 23:37:48 GMT
server: uvicorn
content-length: 0
```

### Validation Error
```
HTTP/1.1 422 Unprocessable Entity
date: Tue, 13 Feb 2024 23:49:59 GMT
server: uvicorn
content-length: 205
content-type: application/json
```
```json
{
  "detail": "Invalid Email (for example)"
}
```

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "path",
        "code"
      ],
      "msg": "String should have at least 4 characters",
      "input": "G",
      "ctx": {
        "min_length": 4
      },
      "url": "https://errors.pydantic.dev/2.6/v/string_too_short"
    }
  ]
}
```

### Internal Server Error

```
HTTP/1.1 500 Internal Server Error
date: Tue, 13 Feb 2024 23:48:58 GMT
server: uvicorn
content-length: 34
content-type: application/json
```

```json
{
  "detail": "Internal Server Error"
}
```

## Technologies Used

- Python - The programming language used for the project.
- REST - The architectural style for building distributed systems, used in the project to create the API.
- FastAPI - The Python framework used in the project to implement the REST API.
- Redis - An in-memory database used in the project for data caching and storing Celery tasks.
- PostgreSQL - A relational database used in the project for data storage.
- SQLAlchemy - An Object-Relational Mapping (ORM) used in the project for working with the database.
- Alembic - A database migration library used in the project to update the database structure when data models
  change.
- Docker - A platform used in the project for creating, deploying, and managing containers, allowing the application
  to run in an isolated environment.

## Technical Specification

A simple RESTful API service for a referral system needs to be developed.

### Functional requirements:

- User registration and authentication (<b>JWT</b>, OAuth 2.0) ✅
- Authenticated users should be able to create or delete their referral code. Only 1 code can be active at a time ✅
- When creating a code, its expiration date must be set ✅
- Ability to retrieve a referral code by the referrer's email address ✅
- Ability to register as a referral using a referral code ✅
- Retrieve information about referrals based on the referrer's ID ✅
- UI documentation (<b>Swagger</b>, ReDoc) ✅

### Optional tasks:

- <strike>Use <a href="clearbit.com/platform/enrichment">clearbit.com/platform/enrichment</a>
to obtain additional user information during registration;</strike>❌
- Use <a href="emailhunter.co">emailhunter.co</a> to verify the specified email address ✅
- Cache referral codes using in-memory database ✅
- Readme.md file with project description and instructions for deployment and testing ✅

### Stack:

- Use any modern web framework ✅
- Use a relational database and migrations (Sqlite, <u><b>PostgreSQL</b></u>, MySQL) ✅
- Host the project on GitHub ✅

### Project requirements:

- Code cleanliness and readability;
- All I/O bound operations should be asynchronous;
- The project should be well-structured;
- The project should be easy to deploy, handle non-standard situations, be resilient to incorrect user actions, etc.