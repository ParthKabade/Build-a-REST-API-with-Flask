# Task 4 – Build a REST API with Flask

## Project Overview

This project implements a RESTful API using **Python and Flask** to manage user data.

The API supports all four CRUD operations:

- **GET** – Retrieve users
- **POST** – Create a new user
- **PUT** – Update an existing user
- **DELETE** – Delete a user

User records are stored in an in-memory Python dictionary. Pydantic is used to validate incoming user data.

## Technologies Used

- Python
- Flask
- Pydantic
- Postman
- JSON

## Project Structure

```text
Task-4/
│
├── app.py
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Task-4
```

### 2. Install dependencies

```bash
pip install flask pydantic
```

### 3. Run the application

```bash
python app.py
```

The Flask server will start at:

```text
http://127.0.0.1:5000
```

## API Endpoints

Base URL: `http://127.0.0.1:5000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | Retrieve all users |
| POST | `/users` | Create a new user |
| PUT | `/users/<user_id>` | Update a user |
| DELETE | `/users/<user_id>` | Delete a user |

### 1. GET – Retrieve Users

**Endpoint:** `GET /users`

Retrieves all existing user records.

Example response:

```json
{
  "message": "Success",
  "users": [
    {
      "username": "johndoe",
      "email": "johndoe@example.com"
    }
  ]
}
```

**Status Code:** `200 OK`

### 2. POST – Create User

**Endpoint:** `POST /users`

Creates a new user with an automatically generated ID.

Example request:

```json
{
  "username": "parth",
  "email": "parth@example.com"
}
```

Example response:

```json
{
  "id": 3,
  "received": {
    "username": "parth",
    "email": "parth@example.com"
  },
  "status": "success"
}
```

**Status Code:** `201 Created`

### 3. PUT – Update User

**Endpoint:** `PUT /users/1`

Updates the username and email of an existing user.

Example request:

```json
{
  "username": "updated_john",
  "email": "updatedjohn@example.com"
}
```

Example response:

```json
{
  "message": "User updated successfully",
  "User": {
    "username": "updated_john",
    "email": "updatedjohn@example.com"
  }
}
```

**Status Code:** `200 OK`

If the user does not exist, the API returns `404 Not Found`.

### 4. DELETE – Delete User

**Endpoint:** `DELETE /users/2`

Deletes an existing user using their ID.

Example response:

```json
{
  "message": "User 2 has been deleted"
}
```

**Status Code:** `200 OK`

If the user does not exist, the API returns `404 Not Found`.

## Data Validation

Pydantic's `ItemSchema` validates incoming user data.

Validation rules:

- `username` is required and must contain at least 2 characters.
- `email` is required and must contain at least 5 characters.

Invalid JSON bodies return `400 Bad Request`.

Validation errors return `422 Unprocessable Entity`.

## Testing

All API endpoints were tested using **Postman**.

Test scenarios included:

- Retrieving users.
- Creating users and generating IDs.
- Updating existing users.
- Handling nonexistent user IDs.
- Validating incorrect input.
- Deleting existing users.
- Verifying deletion through GET requests.

## Important Note

This project uses an in-memory Python dictionary instead of a permanent database.

Therefore, user data and changes are lost when the Flask application restarts.

## Learning Outcomes

- Understanding REST API fundamentals.
- Implementing CRUD operations using Flask.
- Handling HTTP methods and status codes.
- Working with JSON request and response data.
- Validating input using Pydantic.
- Testing REST APIs using Postman.
