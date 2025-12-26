# pragma: no cover

"""Top-level package for RPTodo Project."""
# rptodo/__init__.py

__app_name__ = "rptodo"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_WRITE_ERROR,
    DB_READ_ERROR,
    JSON_ERROR,
    ID_ERROR,
    DESCRIPTION_ERROR,
) = range(8)

MAX_DESCRIPTION_LENGTH = 256

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_WRITE_ERROR: "database write error",
    DB_READ_ERROR: "database read error",
    JSON_ERROR: "json operation error",
    ID_ERROR: "to-do id error",
    DESCRIPTION_ERROR: "Description is between 1 - 255 characters long",
}
