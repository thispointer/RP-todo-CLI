import configparser
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from rptodo_project import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS
from rptodo_project.domain_todo import DBResponse, Priority, ToDoItem

# In case users do not provide a file db path
DEFAULT_DB_FILE_PATH = Path(__file__).parent.parent.joinpath(".default_todo_db.json")


def todo_from_dict(data: dict[str, Any]) -> ToDoItem:
    return ToDoItem(
        id=int(data["id"]),
        description=str(data["description"]),
        priority=Priority(int(data["priority"])),
        completed=bool(data["completed"]),
    )


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r", encoding="utf-8") as db:
                try:
                    raw_list = json.load(db)
                except json.JSONDecodeError:
                    # Wrong JSON format
                    return DBResponse(todo_list=[], error=JSON_ERROR)
        except OSError:
            # File I/O problems (missing file, permissions, etc.)
            return DBResponse(todo_list=[], error=DB_READ_ERROR)

        items: list[ToDoItem] = [todo_from_dict(d) for d in raw_list]
        return DBResponse(todo_list=items, error=SUCCESS)

    def write_todos(self, todo_list: list[ToDoItem]) -> DBResponse:
        # Convert dataclasses to plain dicts first
        serializable_list: list[dict[str, Any]] = []
        for item in todo_list:
            d = asdict(item)
            # Ensure Priority (IntEnum) becomes int for JSON
            d["priority"] = int(item.priority)
            serializable_list.append(d)

        try:
            with self._db_path.open("w", encoding="utf-8") as db:
                json.dump(serializable_list, db, indent=4)
            return DBResponse(todo_list=todo_list, error=SUCCESS)
        except OSError:
            return DBResponse(todo_list=todo_list, error=DB_WRITE_ERROR)


def get_database_path(config_file: Path) -> Path:
    """Retrieves the current database path from the config file."""

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    db_path = Path(config_parser["General"]["Database"])
    return db_path


def init_database(db_path: Path) -> int:
    """Initializes the database file at the specified path."""
    try:
        db_path.write_text("[]", encoding="utf-8")  # Initializes an empty To-Do list

    except OSError:
        return DB_WRITE_ERROR

    return SUCCESS
