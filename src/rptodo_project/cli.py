""" "This module provides the RP To-Do CLI."""
# rptodo/cli.py

from pathlib import Path
from typing import Annotated

import typer

from rptodo_project import (
    ERRORS,
    FILE_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    config,
    database,
)
from rptodo_project.domain_todo import Priority
from rptodo_project.rptodo import Todoer

app = typer.Typer()


@app.command()
def init(
    db_path: Annotated[
        str,
        typer.Option(
            "--db-path",
            "-db",
            prompt="The to-do database location?",
        ),
    ] = str(database.DEFAULT_DB_FILE_PATH),
) -> None:
    """Initializes the to-do database."""
    app_init_code = config.init_app(db_path)
    if app_init_code in ERRORS:
        typer.secho(
            f"Initialization failed with: {ERRORS[app_init_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=app_init_code)

    db_init_code = database.init_database(Path(db_path))
    if db_init_code in ERRORS:
        typer.secho(
            f"Database initialization failed with: {ERRORS[db_init_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=db_init_code)
    else:
        typer.secho(
            f"Initialization successful!\n The to-do database is {db_path}",
            fg=typer.colors.GREEN,
        )


@app.command(name="add")
def add(
    description: Annotated[
        list[str],
        typer.Argument(..., help="The description for the to-do item."),
    ],
    priority: Annotated[
        int,
        typer.Option(
            "--priority",
            "-p",
            min=1,
            max=3,
            help="Priority: 1=low, 2=normal, 3=high.",
        ),
    ] = 2,
) -> None:
    """Add a new to-do item to the database."""
    todoer = get_Todoer()

    # Map int -> Priority enum (simple, explicit)
    try:
        prio = Priority(priority)
    except ValueError:
        typer.secho("Invalid priority value.", fg=typer.colors.RED)
        raise typer.Exit(code=1) from None

    current = todoer.add(description=description, priority=prio)

    if current.error != SUCCESS:
        # Use ERRORS mapping you already import
        msg = ERRORS.get(current.error, "Unknown error")
        typer.secho(f"Error while adding to-do: {msg}", fg=typer.colors.RED)
        raise typer.Exit(code=current.error) from None

    # Success: show what has been added
    item = current.todo
    assert item is not None
    typer.secho(
        f'To-do added: [id={item.id}] "{item.description}" \
            (priority={item.priority.name})',
        fg=typer.colors.GREEN,
    )


@app.command(name="list")
def list_todos() -> None:
    """List all to-do items."""
    todoer = get_Todoer()
    todo_list = todoer.get_todo_list()

    if not todo_list:
        typer.secho("No to-do items found in the database.", fg=typer.colors.CYAN)
        raise typer.Exit(code=SUCCESS) from None

    typer.secho("\nCurrent To-Do list:\n", fg=typer.colors.BLUE, bold=True)
    columns = f"{'ID':>3s} {'Done':^5s} {'Priority':^14s} Description" + " " * 14
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)

    for item in todo_list:
        status = "✔" if item.completed else "▪"
        typer.secho(
            f"{item.id:3d} [{status:^3s}] {item.priority.name:^14s} {item.description}",
            fg=typer.colors.WHITE,
        )
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)


@app.command(name="toggle")
def toggle(
    todo_id: Annotated[
        int,
        typer.Argument(
            ..., help="ID of the to-do item to set or unset the done status."
        ),
    ],
) -> None:
    """Toggle completed/not-completed state of a to-do item."""
    todoer = get_Todoer()
    current = todoer.toggle_done(todo_id)

    if current.error != SUCCESS:
        msg = ERRORS.get(current.error, "Unknown error")
        typer.secho(f"Error toggling to-do: {msg}", fg=typer.colors.RED)
        raise typer.Exit(code=current.error)

    item = current.todo
    assert item is not None
    status = "completed" if item.completed else "not completed"
    typer.secho(
        f"To-do [{item.id}] is now {status}.",
        fg=typer.colors.GREEN,
    )


@app.command(name="remove")
def remove(
    todo_id: Annotated[
        int,
        typer.Argument(..., help="ID of the to-do item to remove."),
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            is_eager=True,
            help="Force removal to-do item without confirmation.",
        ),
    ] = False,
) -> None:
    """Remove a to-do item by provinding its ID."""

    def _remove(id: int) -> None:
        current = todoer.remove(id)

        if current.error != SUCCESS:
            msg = ERRORS.get(current.error, "Unknown error")
            typer.secho(f"Error removing to-do: {msg}", fg=typer.colors.RED)
            raise typer.Exit(code=current.error)

        item = current.todo
        assert item is not None
        typer.secho(
            f'To-do removed: [id={item.id}] "{item.description}"',
            fg=typer.colors.GREEN,
        )

    todoer = get_Todoer()

    if force:
        _remove(todo_id)
    else:
        current = todoer.find(todo_id)
        if current.error != SUCCESS:
            msg = ERRORS.get(current.error, "Unknown error")
            typer.secho(f"Error finding to-do: {msg}", fg=typer.colors.RED)
            raise typer.Exit(code=current.error)
        item = current.todo
        assert item is not None
        delete_confirm = typer.confirm(
            f"Are you sure you want to delete to-do #{item.id}: {item.description}?"
        )
        if delete_confirm:
            _remove(todo_id)
        else:
            typer.echo("Operation cancelled.")


def get_Todoer() -> Todoer:
    """Returns the Todoer CLI app instance."""
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            "Config file not found. Please run 'rptodo init' first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(FILE_ERROR)

    if db_path.exists():
        return Todoer(Path(db_path))
    else:
        typer.secho(
            "Database file not found. Please run 'rptodo init' first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(FILE_ERROR)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Shows the application's version and exits.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """The main entry point for the RP To-Do CLI application."""
    return
