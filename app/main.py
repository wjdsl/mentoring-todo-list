from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Todo List API")

# TODO 리스트 생성 요청
class TodoListCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

# TODO 리스트 응답
class TodoListResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

# TODO 생성 요청
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None

# TODO 응답
class TodoResponse(BaseModel):
    id: int
    todo_list_id: int
    title: str
    description: Optional[str] = None
    completed: bool
    completed_at: Optional[datetime] = None

# TODO 수정 요청
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Todo 리스트 저장 모델
class TodoList(BaseModel):
    id: int
    name: str
    created_at: datetime

# Todo 저장 모델
class Todo(BaseModel):
    id: int
    todo_list_id: int
    title: str
    description: Optional[str] = None
    completed: bool
    completed_at: Optional[datetime] = None

# Todo 리스트 저장소 관리 클래스
class TodoListRepository:
    def __init__(self):
        self.todo_lists: dict[int, TodoList] = {}
        self.next_todo_list_id = 1

# Todo 저장소 관리 클래스
class TodoRepository:
    def __init__(self):
        self.todos: dict[int, Todo] = {}
        self.next_todo_id = 1

todo_list_repository = TodoListRepository()
todo_repository = TodoRepository()

@app.post(
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

@app.post(
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

@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, request: TodoUpdate):

    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = todo_repository.todos[todo_id]

    if request.title is not None:
        todo.title = request.title
    
    if request.description is not None:
        todo.description = request.description

    return todo

@app.post("/todos/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(todo_id: int):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = todo_repository.todos[todo_id]
    todo.completed = True
    todo.completed_at = datetime.now(timezone.utc)

    return todo

@app.post("/todos/{todo_id}/uncomplete", response_model=TodoResponse)
def uncomplete_todo(todo_id: int):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = todo_repository.todos[todo_id]
    todo.completed = False
    todo.completed_at = None
    
    return todo

@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
)
def delete_todo(todo_id: int):
    if todo_id not in todo_repository.todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    del todo_repository.todos[todo_id]

    return {"message": "Todo deleted successfully"}
