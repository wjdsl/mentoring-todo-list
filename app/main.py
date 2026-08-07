from datetime import datetime
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
    completed_at: Optional[datetime] = None

# TODO 업데이트 요청
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# 임시 저장소(DB 대신 사용)
todo_lists: dict[int, TodoListResponse] = {}
todos: dict[int, TodoResponse] = {}

# 자동 증가 id
next_todo_list_id = 1
next_todo_id = 1

@app.get("/")
def root():
    return {"message": "Hello Todo API"}

@app.post(
    "/todo-lists",
    response_model=TodoListResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo_list(request: TodoListCreate):
    global next_todo_list_id
    
    todo_list = TodoListResponse(
        id=next_todo_list_id,
        name=request.name,
        created_at=datetime.now(),
    )

    todo_lists[next_todo_list_id] = todo_list
    next_todo_list_id += 1

    return todo_list

@app.post(
    "/todo-lists/{list_id}/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo(list_id: int, request: TodoCreate):
    global next_todo_id

    if list_id not in todo_lists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list not found",
        )
    
    todo = TodoResponse(
        id=next_todo_id,
        todo_list_id=list_id,
        title=request.title,
        description=request.description,
        completed_at=None,
    )

    todos[next_todo_id] = todo
    next_todo_id += 1

    return todo

@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, request: TodoUpdate):

    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = todos[todo_id]

    if request.title is not None:
        todo.title = request.title
    
    if request.description is not None:
        todo.description = request.description

    todos[todo_id] = todo

    return todo

@app.post("/todos/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = todos[todo_id]
    todo.completed_at = datetime.now()
    
    todos[todo_id] = todo

    return todo

@app.post("/todos/{todo_id}/uncomplete", response_model=TodoResponse)
def uncomplete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = todos[todo_id]
    todo.completed_at = None
    
    return todo

@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    del todos[todo_id]