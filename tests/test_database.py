"""This module tests database.py"""
# tests/test_database.py

import json
from pathlib import Path

from rptodo_project import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, database
from rptodo_project.domain_todo import Priority, ToDoItem


def test_init_database(tmp_path):
    """Test database initialization."""
    db_path = tmp_path / "test.db"
    result = database.init_database(db_path)
    assert result == SUCCESS
    assert db_path.exists()
    assert db_path.read_text() == "[]"


def test_init_database_invalid_path():
    """Test database init with invalid path."""
    invalid_path = Path("/invalid/nonexistent/path/db.json")
    result = database.init_database(invalid_path)
    assert result == DB_WRITE_ERROR


def test_get_database_path(tmp_path):
    """Test retrieving database path from config."""
    config_file = tmp_path / "config.ini"
    db_path = tmp_path / "test.db"

    config_file.write_text(f"[General]\nDatabase = {db_path}")
    result = database.get_database_path(config_file)

    assert result == db_path


def test_read_todos(tmp_path):
    """Test reading todos from database."""
    db_path = tmp_path / "test.db"
    todo_data = [
        {"id": 1, "description": "Test task.", "priority": 2, "completed": False}
    ]
    db_path.write_text(json.dumps(todo_data))

    handler = database.DatabaseHandler(db_path)
    result = handler.read_todos()

    assert result.error == SUCCESS
    assert len(result.todo_list) == 1
    assert result.todo_list[0].description == "Test task."


def test_read_todos_empty(tmp_path):
    """Test reading from empty database."""
    db_path = tmp_path / "test.db"
    db_path.write_text("[]")

    handler = database.DatabaseHandler(db_path)
    result = handler.read_todos()

    assert result.error == SUCCESS
    assert len(result.todo_list) == 0


def test_read_todos_invalid_json(tmp_path):
    """Test reading database with invalid JSON."""
    db_path = tmp_path / "test.db"
    db_path.write_text("invalid json")

    handler = database.DatabaseHandler(db_path)
    result = handler.read_todos()

    assert result.error == JSON_ERROR
    assert len(result.todo_list) == 0


def test_read_todos_missing_file(tmp_path):
    """Test reading from non-existent file."""
    db_path = tmp_path / "nonexistent.db"

    handler = database.DatabaseHandler(db_path)
    result = handler.read_todos()

    assert result.error == DB_READ_ERROR


def test_write_todos(tmp_path):
    """Test writing todos to database."""
    db_path = tmp_path / "test.db"
    db_path.write_text("[]")

    handler = database.DatabaseHandler(db_path)
    todos = [
        ToDoItem(
            id=1, description="Task one.", priority=Priority.NORMAL, completed=False
        ),
        ToDoItem(id=2, description="Task two.", priority=Priority.HIGH, completed=True),
    ]

    result = handler.write_todos(todos)
    assert result.error == SUCCESS

    # Verify written data
    data = json.loads(db_path.read_text())
    assert len(data) == 2
    assert data[0]["description"] == "Task one."
    assert data[1]["completed"] is True


def test_write_todos_invalid_path():
    """Test writing to invalid path."""
    db_path = Path("/invalid/path/db.json")
    handler = database.DatabaseHandler(db_path)

    todos = [ToDoItem(id=1, description="Task.", priority=Priority.NORMAL)]
    result = handler.write_todos(todos)

    assert result.error == DB_WRITE_ERROR


def test_todo_from_dict():
    """Test converting dict to ToDoItem."""
    data = {"id": 1, "description": "Test.", "priority": 2, "completed": False}
    todo = database.todo_from_dict(data)

    assert todo.id == 1
    assert todo.description == "Test."
    assert todo.priority == Priority.NORMAL
    assert todo.completed is False
