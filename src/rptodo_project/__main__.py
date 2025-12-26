# pragma: no cover
"""RP To-DO entry point script."""
# rptodo/__main__.py

from rptodo_project import __app_name__, cli  # pragma: no cover


def main() -> None:  # pragma: no cover
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":  # pragma: no cover
    main()
