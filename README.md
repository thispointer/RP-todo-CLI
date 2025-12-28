# RPToDo - A Command-Line To-Do Manager

![Python Version](https://img.shields.io/badge/python-3.12-blue)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/thispointer/RP-todo-CLI/actions/workflows/ci.yml/badge.svg?branch=trunk)](https://github.com/thispointer/RP-todo-CLI/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/thispointer/RP-todo-CLI/graph/badge.svg?token=GRDWM697US)](https://codecov.io/github/thispointer/RP-todo-CLI)


A simple, efficient to-do list manager built with Python and Typer.

## Features

- ✅ Add, list, toggle, and remove to-do items
- 🎯 Three priority levels (Low, Normal, High)
- 💾 JSON-based persistent storage
- 🔒 Confirmation prompts for destructive operations
- 📝 Clean CLI interface

## Installation

```bash
uv venv
uv sync
```

## Usage

```bash
# Initialize the database
uv run rptodo-project init

# Add a to-do
uv run rptodo-project add "Buy groceries" --priority 2

# List all to-dos
uv run rptodo-project list

# Toggle completion status
uv run rptodo-project toggle 1

# Remove a to-do (with confirmation)
uv run rptodo-project remove 1

# Force remove without confirmation
uv run rptodo-project remove 1 --force

# Show version
uv run rptodo-project --version
```

## Development

```bash
# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src/rptodo_project -v

# Code linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## Project Structure

```
src/rptodo_project/
├── __init__.py          # Error constants and app metadata
├── __main__.py          # Entry point
├── cli.py              # CLI commands
├── config.py           # Configuration management
├── database.py         # Data persistence
├── domain_todo.py      # Domain models
└── rptodo.py           # Business logic
```

## Code Coverage Tests

[![Codecov](https://codecov.io/github/thispointer/RP-todo-CLI/graphs/sunburst.svg?token=GRDWM697US)
