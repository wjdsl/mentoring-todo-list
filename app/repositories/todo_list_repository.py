from app.models.todo_list import TodoList

# Todo 리스트 저장소 관리 클래스
class TodoListRepository:
    def __init__(self):
        self.todo_lists: dict[int, TodoList] = {}
        self.next_todo_list_id = 1