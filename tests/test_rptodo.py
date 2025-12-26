"""This module tests rptodo.py"""
# tests/test_rptodo.py

from pathlib import Path

import pytest

from rptodo_project import DESCRIPTION_ERROR, ID_ERROR, MAX_DESCRIPTION_LENGTH, SUCCESS
from rptodo_project.database import DatabaseHandler
from rptodo_project.domain_todo import Priority
from rptodo_project.rptodo import Todoer


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Create a temporary database."""
    path = tmp_path / "test.db"
    DatabaseHandler(path).write_todos([])
    return path


@pytest.fixture
def todoer(db_path: Path) -> Todoer:
    """Create a Todoer instance with temporary database."""
    return Todoer(db_path)


def test_add_success(todoer: Todoer) -> None:
    """Test successfully adding a to-do."""
    result = todoer.add(["Buy", "groceries"], Priority.HIGH)
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.id == 1
    assert result.todo.description == "Buy groceries."
    assert result.todo.priority == Priority.HIGH


def test_add_default_priority(todoer: Todoer) -> None:
    """Test adding with default priority."""
    result = todoer.add(["Task"])
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.priority == Priority.NORMAL


def test_add_adds_period(todoer: Todoer) -> None:
    """Test that period is added to description."""
    result = todoer.add(["Task", "without", "period"])
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.description == "Task without period."


def test_add_already_has_period(todoer: Todoer) -> None:
    """Test description that already has period."""
    result = todoer.add(["Task."])
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.description == "Task."


def test_add_empty_description(todoer: Todoer) -> None:
    """Test adding with empty description."""
    result = todoer.add([])
    assert result.error == DESCRIPTION_ERROR
    assert result.todo is None


def test_add_whitespace_only(todoer: Todoer) -> None:
    """Test adding with only whitespace."""
    result = todoer.add(["   ", "  "])
    assert result.error == DESCRIPTION_ERROR
    assert result.todo is None


def test_add_description_too_long(todoer: Todoer) -> None:
    """Test adding with description exceeding max length."""
    long_text = "a" * (MAX_DESCRIPTION_LENGTH + 1)
    result = todoer.add([long_text])
    assert result.error == DESCRIPTION_ERROR
    assert result.todo is None


def test_add_description_at_max_length(todoer: Todoer) -> None:
    """Test adding with description at max length."""
    text = "a" * (MAX_DESCRIPTION_LENGTH - 1)
    result = todoer.add([text])
    assert result.error == SUCCESS
    assert result.todo is not None
    assert len(result.todo.description) == MAX_DESCRIPTION_LENGTH


def test_add_multiple_todos(todoer: Todoer) -> None:
    """Test adding multiple todos increments id."""
    result1 = todoer.add(["First"])
    result2 = todoer.add(["Second"])
    result3 = todoer.add(["Third"])

    assert result1.todo is not None
    assert result2.todo is not None
    assert result3.todo is not None
    assert result1.todo.id == 1
    assert result2.todo.id == 2
    assert result3.todo.id == 3


def test_get_todo_list(todoer: Todoer) -> None:
    """Test getting the todo list."""
    todoer.add(["Task", "one"], Priority.LOW)
    todoer.add(["Task", "two"], Priority.HIGH)

    todos = todoer.get_todo_list()
    assert len(todos) == 2
    assert todos[0].description == "Task one."
    assert todos[1].description == "Task two."


def test_get_todo_list_empty(todoer: Todoer) -> None:
    """Test getting empty todo list."""
    todos = todoer.get_todo_list()
    assert todos == []


def test_get_todo_list_on_read_error(todoer: Todoer) -> None:
    """Test get_todo_list returns empty on read error."""
    db_path = todoer._db_handler._db_path
    db_path.write_text("invalid json")

    todos = todoer.get_todo_list()
    assert todos == []


def test_toggle_done_success(todoer: Todoer) -> None:
    """Test toggling todo completion status."""
    todoer.add(["Task"])
    result = todoer.toggle_done(1)

    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.completed is True


def test_toggle_done_twice(todoer: Todoer) -> None:
    """Test toggling twice reverts to incomplete."""
    todoer.add(["Task"])
    todoer.toggle_done(1)
    result = todoer.toggle_done(1)

    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.completed is False


def test_toggle_done_invalid_id(todoer: Todoer) -> None:
    """Test toggling with invalid (non-existent) id."""
    result = todoer.toggle_done(999)
    assert result.error == ID_ERROR
    assert result.todo is None


def test_toggle_done_zero_id(todoer: Todoer) -> None:
    """Test toggling with id <= 0."""
    result = todoer.toggle_done(0)
    assert result.error == ID_ERROR
    assert result.todo is None


def test_toggle_done_negative_id(todoer: Todoer) -> None:
    """Test toggling with negative id."""
    result = todoer.toggle_done(-5)
    assert result.error == ID_ERROR
    assert result.todo is None


def test_remove_success(todoer: Todoer) -> None:
    """Test removing a todo."""
    todoer.add(["Task", "to", "remove"])
    result = todoer.remove(1)

    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.description == "Task to remove."

    todos = todoer.get_todo_list()
    assert len(todos) == 0


def test_remove_invalid_id(todoer: Todoer) -> None:
    """Test removing with non-existent id."""
    todoer.add(["Task"])
    result = todoer.remove(999)

    assert result.error == ID_ERROR
    assert result.todo is None

    todos = todoer.get_todo_list()
    assert len(todos) == 1


def test_remove_zero_id(todoer: Todoer) -> None:
    """Test removing with id <= 0."""
    todoer.add(["Task"])
    result = todoer.remove(0)

    assert result.error == ID_ERROR
    assert result.todo is None


def test_remove_negative_id(todoer: Todoer) -> None:
    """Test removing with negative id."""
    todoer.add(["Task"])
    result = todoer.remove(-10)

    assert result.error == ID_ERROR
    assert result.todo is None


def test_remove_multiple_todos(todoer: Todoer) -> None:
    """Test removing from a list of multiple todos."""
    todoer.add(["First"])
    todoer.add(["Second"])
    todoer.add(["Third"])

    result = todoer.remove(2)
    assert result.error == SUCCESS
    assert result.todo is not None

    todos = todoer.get_todo_list()
    assert len(todos) == 2
    assert todos[0].id == 1
    assert todos[1].id == 3


def test_find_success(todoer: Todoer) -> None:
    """Test finding a todo by id."""
    todoer.add(["Task", "one"], Priority.LOW)
    todoer.add(["Task", "two"], Priority.HIGH)

    result = todoer.find(1)
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.id == 1
    assert result.todo.description == "Task one."
    assert result.todo.priority == Priority.LOW


def test_find_not_found(todoer: Todoer) -> None:
    """Test finding non-existent todo."""
    todoer.add(["Task"])
    result = todoer.find(999)

    assert result.error == ID_ERROR
    assert result.todo is None


def test_find_zero_id(todoer: Todoer) -> None:
    """Test finding with id <= 0."""
    todoer.add(["Task"])
    result = todoer.find(0)

    assert result.error == ID_ERROR
    assert result.todo is None


def test_find_negative_id(todoer: Todoer) -> None:
    """Test finding with negative id."""
    todoer.add(["Task"])
    result = todoer.find(-1)

    assert result.error == ID_ERROR
    assert result.todo is None


def test_find_from_multiple(todoer: Todoer) -> None:
    """Test finding specific todo from multiple todos."""
    todoer.add(["First"])
    todoer.add(["Second"])
    todoer.add(["Third"])

    result = todoer.find(2)
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.description == "Second."


def test_add_with_corrupted_db(todoer: Todoer) -> None:
    """Test add still creates todo when database is corrupted."""
    # Add a todo first
    todoer.add(["Original"])

    # Corrupt the database
    db_path = todoer._db_handler._db_path
    db_path.write_text("invalid json")

    # Try to add another todo - should still succeed
    result = todoer.add(["New", "task"])
    assert result.error == SUCCESS
    assert result.todo is not None
    assert result.todo.description == "New task."
