from app.models.todo import Todo

# Todo 저장소 관리 클래스
class TodoRepository:
    def __init__(self):
        self.todos: dict[int, Todo] = {}
        self.next_todo_id = 1