"""This Module provides the RP To-Do model-controller"""
# rptodo_projects/rptodo.py

from pathlib import Path

from rptodo_project import (  # your error constants
    DB_READ_ERROR,
    DESCRIPTION_ERROR,
    ID_ERROR,
    MAX_DESCRIPTION_LENGTH,
    SUCCESS,
)
from rptodo_project.database import DatabaseHandler
from rptodo_project.domain_todo import CurrentTodo, Priority, ToDoItem


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(
        self, description: list[str], priority: Priority = Priority.NORMAL
    ) -> CurrentTodo:
        """Add a todo and return CurrentTodo with error code."""
        text = " ".join(description).strip()
        if not text:
            return CurrentTodo(todo=None, error=DESCRIPTION_ERROR)

        if len(text) > MAX_DESCRIPTION_LENGTH:
            return CurrentTodo(todo=None, error=DESCRIPTION_ERROR)

        if not text.endswith("."):
            text += "."

        # 1. Read current list from DB
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            # Could not read DB; still return a ToDoItem with a provisional id
            todo = ToDoItem(id=1, description=text, priority=priority)
            return CurrentTodo(todo=todo, error=read.error)

        # 2. Compute next id
        next_id = max((t.id for t in read.todo_list), default=0) + 1
        todo = ToDoItem(id=next_id, description=text, priority=priority)

        # 3. Append and write back
        new_list = list(read.todo_list) + [todo]
        write = self._db_handler.write_todos(new_list)

        return CurrentTodo(todo=todo, error=write.error)

    def get_todo_list(self) -> list[ToDoItem]:
        """
        Return the current todo list (or empty list on read error).
        """
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return []
        return list(read.todo_list)

    def toggle_done(self, todo_id: int) -> CurrentTodo:
        """Flip completed state of a to-do item by id."""
        if todo_id <= 0:
            return CurrentTodo(todo=None, error=ID_ERROR)
        read = self._db_handler.read_todos()
        if read.error != SUCCESS:
            return CurrentTodo(todo=None, error=read.error)

        # find item by id, not by position
        try:
            index = next(
                i for i, item in enumerate(read.todo_list) if item.id == todo_id
            )
        except StopIteration:
            return CurrentTodo(todo=None, error=ID_ERROR)

        old_item = read.todo_list[index]
        new_item = ToDoItem(
            id=old_item.id,
            description=old_item.description,
            priority=old_item.priority,
            completed=not old_item.completed,
        )

        new_list = list(read.todo_list)
        new_list[index] = new_item

        write = self._db_handler.write_todos(new_list)
        return CurrentTodo(todo=new_item, error=write.error)

    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do item by id."""
        if todo_id <= 0:
            return CurrentTodo(todo=None, error=ID_ERROR)

        read = self._db_handler.read_todos()
        if read.error != SUCCESS:
            return CurrentTodo(todo=None, error=read.error)

        # find item by id, not by position
        try:
            index = next(
                i for i, item in enumerate(read.todo_list) if item.id == todo_id
            )
        except StopIteration:
            return CurrentTodo(todo=None, error=ID_ERROR)

        new_list = list(read.todo_list)
        removed_item = new_list.pop(index)

        write = self._db_handler.write_todos(new_list)
        return CurrentTodo(todo=removed_item, error=write.error)

    def find(self, todo_id: int) -> CurrentTodo:
        """Find a to-do item by id."""
        read = self._db_handler.read_todos()
        if read.error != SUCCESS:
            return CurrentTodo(todo=None, error=read.error)

        # find item by id, not by position
        try:
            index = next(
                i for i, item in enumerate(read.todo_list) if item.id == todo_id
            )
        except StopIteration:
            return CurrentTodo(todo=None, error=ID_ERROR)

        return CurrentTodo(todo=read.todo_list[index], error=SUCCESS)
