from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.models.todo import Todo, TodoCreate, TodoResponse, TodoUpdate
from app.repositories import todo_list_repository, todo_repository


router = APIRouter()


@router.post(
    "/todo-lists/{list_id}/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo(list_id: int, request: TodoCreate):
    if list_id not in todo_list_repository.todo_lists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo list not found",
        )

    todo = Todo(
        id=todo_repository.next_todo_id,
        todo_list_id=list_id,
        title=request.title,
        description=request.description,
        completed=False,
        completed_at=None,
    )

    todo_repository.todos[todo_repository.next_todo_id] = todo
    todo_repository.next_todo_id += 1

    return todo


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, request: TodoUpdate):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo not found",
        )

    todo = todo_repository.todos[todo_id]

    if request.title is not None:
        todo.title = request.title

    if request.description is not None:
        todo.description = request.description

    return todo


@router.post("/todos/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(todo_id: int):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo not found",
        )

    todo = todo_repository.todos[todo_id]
    todo.completed = True
    todo.completed_at = datetime.now(timezone.utc)

    return todo


@router.post("/todos/{todo_id}/uncomplete", response_model=TodoResponse)
def uncomplete_todo(todo_id: int):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo not found",
        )

    todo = todo_repository.todos[todo_id]
    todo.completed = False
    todo.completed_at = None

    return todo


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
)
def delete_todo(todo_id: int):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo not found",
        )

    del todo_repository.todos[todo_id]

    return {"message": "Todo deleted successfully"}
