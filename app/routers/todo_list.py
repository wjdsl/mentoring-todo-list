from datetime import datetime, timezone

from fastapi import APIRouter, status

from app.models.todo_list import TodoList, TodoListCreate, TodoListResponse
from app.repositories import todo_list_repository


router = APIRouter()


@router.post(
    "/todo-lists",
    response_model=TodoListResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo_list(request: TodoListCreate):
    todo_list = TodoList(
        id=todo_list_repository.next_todo_list_id,
        name=request.name,
        created_at=datetime.now(timezone.utc),
    )

    todo_list_repository.todo_lists[
        todo_list_repository.next_todo_list_id
    ] = todo_list
    todo_list_repository.next_todo_list_id += 1

    return todo_list
