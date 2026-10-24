from datetime import datetime, timezone
from typing import Annotated, Any
from collections.abc import Sequence

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.dependencies import get_task_store
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI(
    title="Task Management API",
    description="A Basic RESTful API for managing tasks",
    version="1.0.0",
)

app.state.tasks = {}
app.state.next_task_id = 1

class ErrorDetail(BaseModel):
    code: str
    message: str 
    details: list[dict] | None = None

class ErrorBox(BaseModel):
    error: ErrorDetail

def error_response(
    code: str,
    message: str,
    details: Sequence[Any] | None = None,
) -> dict:

    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }

@app.exception_handler(HTTPException)
async def http_error_handler(
    request: Request,
    exc: HTTPException,
):
    codes = {
        404: "NOT_FOUND",
        409: "CONFLICT",
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            codes.get(exc.status_code, "HTTP_ERROR"),
            str(exc.detail),
        ),
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            "VALIDATION_ERROR",
            "Request validation failed.",
            exc.errors(),
        ),
    )

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={422: {"model": ErrorBox}},
)

def create_task(
    payload: TaskCreate,
    request: Request,
    tasks: Annotated[dict, Depends(get_task_store)],
):
    task_id = request.app.state.next_task_id

    task = {
        "id": task_id,
        "title": payload.title,
        "description": payload.description,
        "completed": False,
        "created_at": datetime.now(timezone.utc)
    }

    tasks[task_id] = task
    request.app.state.next_task_id += 1

    return task

@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def list_tasks(
    tasks: Annotated[dict, Depends(get_task_store)]
):
    return list(tasks.values())

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    responses={404: {"model": ErrorBox}},
)
def get_task(
    task_id: int,
    tasks: Annotated[dict, Depends(get_task_store)],
):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    return task

@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    responses={404: {"model": ErrorBox}},
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    tasks: Annotated[dict, Depends(get_task_store)],
):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    changes = payload.model_dump(exclude_unset=True)
    task.update(changes)

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorBox}},
)
def del_task(
    task_id: int,
    tasks: Annotated[dict, Depends(get_task_store)],
):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    del tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)