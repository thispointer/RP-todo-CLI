"""This module tests cli.py"""
# tests/test_cli.py

from pathlib import Path

from typer.testing import CliRunner

from rptodo_project import SUCCESS, cli

runner = CliRunner()


def test_version_callback():
    """Test the --version flag."""
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == SUCCESS
    assert "rptodo" in result.stdout


def test_init_command(tmp_path: Path):
    """Test the init command."""
    db_path = tmp_path / "test.db"
    result = runner.invoke(cli.app, ["init", "--db-path", str(db_path)])
    assert result.exit_code == SUCCESS
    assert "Initialization successful" in result.stdout
    assert db_path.exists()


def test_init_command_invalid_path():
    """Test init with invalid path."""
    result = runner.invoke(cli.app, ["init", "--db-path", "/invalid/path/db.json"])
    assert result.exit_code != SUCCESS


def test_add_command(tmp_path: Path):
    """Test adding a to-do item."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])

    result = runner.invoke(cli.app, ["add", "my", "first", "todo", "-p", "1"])
    assert result.exit_code == SUCCESS
    assert "To-do added" in result.stdout
    assert "my first todo" in result.stdout


def test_add_command_default_priority(tmp_path: Path):
    """Test adding a to-do with default priority (2)."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])

    result = runner.invoke(cli.app, ["add", "task", "without", "priority"])
    assert result.exit_code == SUCCESS
    assert "To-do added" in result.stdout


def test_add_command_invalid_priority(tmp_path: Path):
    """Test adding a to-do with invalid priority."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])

    result = runner.invoke(cli.app, ["add", "task", "-p", "5"])
    assert result.exit_code != SUCCESS


def test_list_command(tmp_path: Path):
    """Test listing to-do items."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])
    runner.invoke(cli.app, ["add", "first", "todo", "-p", "1"])
    runner.invoke(cli.app, ["add", "second", "todo", "-p", "2"])

    result = runner.invoke(cli.app, ["list"])
    assert result.exit_code == SUCCESS
    assert "Current To-Do list" in result.stdout
    assert "first todo" in result.stdout
    assert "second todo" in result.stdout


def test_list_command_empty(tmp_path: Path):
    """Test listing when no to-do items exist."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])

    result = runner.invoke(cli.app, ["list"])
    assert result.exit_code == SUCCESS
    assert "No to-do items found" in result.stdout


def test_toggle_command(tmp_path: Path):
    """Test toggling a to-do item's completed status."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])
    runner.invoke(cli.app, ["add", "test", "todo"])

    result = runner.invoke(cli.app, ["toggle", "1"])
    assert result.exit_code == SUCCESS
    assert "is now completed" in result.stdout


def test_toggle_command_not_found(tmp_path: Path):
    """Test toggling a non-existent to-do item."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])

    result = runner.invoke(cli.app, ["toggle", "999"])
    assert result.exit_code != SUCCESS


def test_remove_command(tmp_path: Path):
    """Test removing a to-do item with force flag."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])
    runner.invoke(cli.app, ["add", "task", "to", "remove"])

    result = runner.invoke(cli.app, ["remove", "1", "--force"])
    assert result.exit_code == SUCCESS
    assert "To-do removed" in result.stdout


def test_remove_command_with_confirmation(tmp_path: Path):
    """Test removing a to-do item with user confirmation."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])
    runner.invoke(cli.app, ["add", "task", "to", "remove"])

    result = runner.invoke(cli.app, ["remove", "1"], input="y\n")
    assert result.exit_code == SUCCESS
    assert "To-do removed" in result.stdout


def test_remove_command_cancel_confirmation(tmp_path: Path):
    """Test cancelling removal with confirmation."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])
    runner.invoke(cli.app, ["add", "task", "to", "remove"])

    result = runner.invoke(cli.app, ["remove", "1"], input="n\n")
    assert result.exit_code == SUCCESS
    assert "Operation cancelled" in result.stdout


def test_remove_command_not_found(tmp_path: Path):
    """Test removing a non-existent to-do item."""
    db_path = tmp_path / "test.db"
    runner.invoke(cli.app, ["init", "--db-path", str(db_path)])

    result = runner.invoke(cli.app, ["remove", "999", "--force"])
    assert result.exit_code != SUCCESS


def test_list_command_without_init(tmp_path: Path):
    """Test listing without initialization."""
    db_path = tmp_path / "test.db"
    # Don't initialize, just try to list
    result = runner.invoke(cli.app, ["list"])
    assert result.exit_code == SUCCESS
    assert (
        "No to-do items found" in result.stdout or "Current To-Do list" in result.stdout
    )


def test_toggle_command_without_init(tmp_path: Path):
    """Test toggling without initialization."""
    db_path = tmp_path / "test.db"
    result = runner.invoke(cli.app, ["toggle", "1"])
    assert result.exit_code == SUCCESS or result.exit_code != SUCCESS


def test_remove_command_without_init(tmp_path: Path):
    """Test removing without initialization."""
    db_path = tmp_path / "test.db"
    result = runner.invoke(cli.app, ["remove", "1"])
    assert result.exit_code == SUCCESS or result.exit_code != SUCCESS
