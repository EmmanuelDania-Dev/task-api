# Task Management API

A RESTful API built with **FastAPI and Pydantic** to demonstrate API design, request validation, dependency injection, structured error handling, HTTP status codes, and automatic OpenAPI documentation.

## Features

- CRUD operations for task management.
- Pydantic request and response schemas.
- Input validation and structured validation errors.
- Dependency injection using `Depends()`.
- Consistent JSON error responses.
- Appropriate HTTP status codes.
- Automatically generated API documentation.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

## Project Structure

```text
task-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── dependencies.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git

### 1. Clone the repository

```bash
git clone https://github.com/EmmanuelDania-Dev/task-api.git
```

### 2. Navigate to the project root

```bash
cd task-api
```

Run the remaining commands from this directory.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PATCH | `/tasks/{task_id}` | Update selected task fields |
| DELETE | `/tasks/{task_id}` | Delete a task |

### HTTP Status Codes

- `200 OK` — Request completed successfully.
- `201 Created` — Task created successfully.
- `204 No Content` — Task deleted successfully.
- `404 Not Found` — Task does not exist.
- `422 Unprocessable Entity` — Request data failed validation.

## API Documentation

FastAPI automatically generates interactive documentation and an OpenAPI specification.

With the server running, visit:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

Use Swagger UI to explore the endpoints, submit requests, and inspect responses.

## Storage

Tasks are stored in memory. Data is lost when the server restarts.

## Demo

This is a demo recording of the API running successfully:
https://drive.google.com/file/d/1h-idsbcOu1FL_RihmTrEvgPojxUUd-qP/view?usp=sharing

## Project Objective

This project demonstrates practical application of RESTful API design, Pydantic validation, dependency injection, structured error handling, and automatic API documentation using FastAPI.
