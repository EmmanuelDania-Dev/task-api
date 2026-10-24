from fastapi import Request

def get_task_store(request: Request) -> dict:
    return request.app.state.tasks