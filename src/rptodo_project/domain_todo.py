# pragma: no cover

"""Domain objects for RPToDo Project."""
# rptodo_project/domain_todo.py

from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum, unique


@unique
class Priority(IntEnum):
    NONE = 0
    LOW = 1
    NORMAL = 2
    HIGH = 3


@dataclass(frozen=True)
class ToDoItem:
    id: int
    description: str
    priority: Priority
    completed: bool = False


@dataclass(frozen=True)
class CurrentTodo:
    todo: ToDoItem | None
    error: int


@dataclass(frozen=True)
class DBResponse:
    todo_list: Sequence[ToDoItem]
    error: int
