# RPToDo - A Command-Line To-Do Manager

![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/thispointer/RP-todo-CLI/actions/workflows/ci.yml/badge.svg?branch=trunk)](https://github.com/thispointer/RP-todo-CLI/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/thispointer/RP-todo-CLI/graph/badge.svg?token=GRDWM697US)](https://codecov.io/github/thispointer/RP-todo-CLI)
![Status](https://img.shields.io/badge/status-demo%20only-orange)
![Security](https://img.shields.io/badge/security-not%20production%20ready-red)

> A command-line to-do list manager built with Python and Typer, demonstrating modern Python development practices.

## 📚 About This Project

This project is based on the excellent [Real Python video course](https://realpython.com/courses/build-command-line-todo-app-typer/) **"Building a Python Command-Line To-Do App With Typer"** by Emmanuel Nwokocha and team. The [original tutorial](https://realpython.com/python-typer-cli/) by Leonidas Pozo Ramos provides a great introduction to building CLI applications with Python and Typer.

### What Makes This Version Different?

This implementation extends the original tutorial with several improvements that follow modern Python best practices:

#### 🔧 Technical Improvements

1. **Immutable Domain Models with Dataclasses**
   - Replaced `NamedTuple` with `@dataclass(frozen=True)` for better type safety
   - Stronger IDE support and more explicit domain modeling
   - Easier to extend with methods and validation

2. **Clear Domain Layer Separation**
   - Introduced explicit domain types: `ToDoItem`, `CurrentTodo`, `DBResponse`
   - Replaced `dict[str, Any]` with proper typed dataclasses
   - Better separation between data models and business logic

3. **Enhanced Type Safety**
   - Full type hints throughout the codebase
   - Type checking with Pyright in CI/CD
   - Priority system using `IntEnum` instead of plain integers

4. **Modern Development Tooling**
   - Uses [uv](https://github.com/astral-sh/uv) for fast dependency management
   - [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
   - Pre-commit hooks for code quality
   - GitHub Actions CI/CD with branch coverage testing

#### 🎯 Why These Changes?

The original tutorial uses `NamedTuple` and dictionaries, which work well for learning. However, for real-world projects:
- **Immutable dataclasses** prevent accidental state changes
- **Explicit domain types** make the code easier to understand and maintain
- **Strong typing** catches bugs at development time instead of runtime

Dataclasses (introduced in Python 3.7 via [PEP 557](https://peps.python.org/pep-0557/)) provide a clean way to define data structures with less boilerplate than traditional classes while maintaining full type safety.

## ⚠️ Important Security Warnings

**This is a demonstration project for learning purposes only. Do not use in production!**

### Security Limitations

1. **No Authentication or Authorization**
   - Anyone with file access can read/modify your to-do list
   - Suitable only for single-user, local development

2. **Plain JSON Storage**
   - Database is a simple JSON file (`.default_todo_db.json`)
   - **Must be stored on a secure, local drive**
   - No encryption, no access controls, no audit logging

3. **No Input Validation Beyond Basic Checks**
   - Limited protection against malformed input
   - Production apps need comprehensive validation

4. **File System Dependencies**
   - Requires write access to local filesystem
   - No concurrent access protection (race conditions possible)

### For Production Use

A production-ready to-do application would require:
- ✅ Proper database (PostgreSQL, SQLite with proper locking, etc.)
- ✅ User authentication and authorization
- ✅ Data encryption at rest and in transit
- ✅ Input validation and sanitization
- ✅ Rate limiting and abuse prevention
- ✅ Audit logging
- ✅ Backup and recovery mechanisms

## ✨ Features

- ✅ Add, list, toggle, and remove to-do items
- 🎯 Three priority levels (Low, Normal, High)
- 💾 JSON-based persistent storage
- 🔒 Confirmation prompts for destructive operations
- 🧪 100% branch coverage with pytest
- 🎨 Type-safe with Pyright
- ⚡ Fast dependency management with uv

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup Project

```bash
# Clone the repository
git clone https://github.com/thispointer/RP-todo-CLI.git
cd RP-todo-CLI

# Create virtual environment and install dependencies
uv sync

# Initialize the database
uv run rptodo-project init
```

## 📖 Usage

### Basic Commands

```bash
# Add a to-do item (default priority: Normal)
uv run rptodo-project add "Buy groceries"

# Add with specific priority (1=Low, 2=Normal, 3=High)
uv run rptodo-project add "Important meeting" --priority 3

# List all to-do items
uv run rptodo-project list

# Mark item as completed (toggle)
uv run rptodo-project toggle 1

# Remove a to-do (asks for confirmation)
uv run rptodo-project remove 1

# Force remove without confirmation
uv run rptodo-project remove 1 --force

# Show version
uv run rptodo-project --version
```

### Example Session

```bash
$ uv run rptodo-project add "Read Python documentation" -p 2
To-do added: [id=1] "Read Python documentation." (priority=NORMAL)

$ uv run rptodo-project add "Deploy to production" -p 3
To-do added: [id=2] "Deploy to production." (priority=HIGH)

$ uv run rptodo-project list

Current To-Do list:

 ID  Done    Priority      Description
-------------------------------------------------
  1  [▪]      NORMAL       Read Python documentation.
  2  [▪]       HIGH        Deploy to production.
-------------------------------------------------

$ uv run rptodo-project toggle 1
To-do [1] is now completed.

$ uv run rptodo-project list

Current To-Do list:

 ID  Done    Priority      Description
-------------------------------------------------
  1  [✓]      NORMAL       Read Python documentation.
  2  [▪]       HIGH        Deploy to production.
-------------------------------------------------
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov --cov-branch --cov-report=term-missing

# Run with HTML coverage report
uv run pytest --cov --cov-branch --cov-report=html
# Open htmlcov/index.html in your browser
```

### Code Quality Checks

```bash
# Run linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Check formatting
uv run ruff format --check .

# Apply formatting
uv run ruff format .

# Type checking
uv run pyright

# Run all checks (same as pre-commit)
uv run pre-commit run --all-files
```

## 📁 Project Structure

```
rptodo-project/
├── src/
│   └── rptodo_project/
│       ├── __init__.py       # Error constants and metadata
│       ├── __main__.py       # Application entry point
│       ├── cli.py            # Typer CLI commands
│       ├── config.py         # Configuration management
│       ├── database.py       # JSON database handler
│       ├── domain_todo.py    # Domain models (dataclasses)
│       └── rptodo.py         # Business logic (Todoer class)
├── tests/                    # Test suite
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── pyproject.toml           # Project dependencies and config
├── uv.lock                  # Locked dependencies
└── README.md
```

## 🏗️ Architecture

### Domain Layer (`domain_todo.py`)

Immutable dataclasses representing core business concepts:

```python
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
```

**Why immutable?**
- Prevents accidental modification
- Clear separation: only `Todoer` can create new states
- Easier to reason about and test

### Business Logic Layer (`rptodo.py`)

The `Todoer` class handles all business logic:
- Adding/removing to-dos
- Toggling completion status
- ID management (auto-increment)
- Error handling

### Persistence Layer (`database.py`)

`DatabaseHandler` manages JSON serialization:
- Reads/writes to-do lists from/to JSON
- Converts between domain objects and JSON
- Handles file I/O errors

### Presentation Layer (`cli.py`)

Typer-based CLI:
- User-friendly command interface
- Color-coded output
- Confirmation prompts for destructive operations

## 🧪 Testing

Current coverage: **~85%** with branch coverage enabled.

```bash
# Run tests with detailed output
uv run pytest -v

# Generate coverage report
uv run pytest --cov --cov-report=html

# View coverage in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 🔄 CI/CD

This project uses GitHub Actions for continuous integration:

- ✅ Linting (Ruff)
- ✅ Formatting check (Ruff)
- ✅ Type checking (Pyright)
- ✅ Tests with branch coverage (Python 3.12 & 3.13)
- ✅ Build verification
- ✅ Coverage reporting (Codecov)

See [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) for details.

## 📊 Code Coverage

[![Codecov Sunburst](https://codecov.io/github/thispointer/RP-todo-CLI/graphs/sunburst.svg?token=GRDWM697US)](https://codecov.io/github/thispointer/RP-todo-CLI)

Interactive coverage reports available at [Codecov](https://codecov.io/github/thispointer/RP-todo-CLI).

## 📚 Learn More

- [Original Real Python Tutorial](https://realpython.com/python-typer-cli/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Leodanis Pozo Ramos** for the excellent [Real Python tutorial](https://realpython.com/python-typer-cli/)
- **Real Python** team for their high-quality educational content
- **Typer** by Sebastián Ramírez for the amazing CLI framework
- **Astral** team for uv and Ruff

---

**Note:** This project is for educational purposes. For production use, consider frameworks like [FastAPI](https://fastapi.tiangolo.com/) with proper database backends, authentication, and security measures.
