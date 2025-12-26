"""This module provides the RPO To-Do config functionality"""
# rptodo/config.py

import configparser
from pathlib import Path

from rptodo_project import (
    DB_WRITE_ERROR,
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
)

# import typer


# for sake of simplicity: config file in root of project folder
CONFIG_DIR_PATH = Path(__file__).parent.parent
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def _init_config_file() -> int:  # pragma: no cover
    """Initializes the config file with default settings."""
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR

    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR

    return SUCCESS


def _create_database(db_path: str) -> int:  # pragma: no cover
    """Creates an empty database file at the specified path."""
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"Database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as config_file:
            config_parser.write(config_file)
    except OSError:
        return DB_WRITE_ERROR

    return SUCCESS


def init_app(db_path: str) -> int:
    """Initializes the RP To-Do application with the specified database path."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code

    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code

    return SUCCESS
