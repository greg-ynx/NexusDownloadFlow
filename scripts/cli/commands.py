"""All CLI commands of Nexus Download Flow."""

from typing import Annotated, List, Optional

import typer
from typer import Typer

from scripts.cli.add_templates.add_templates import cli_add_templates
from scripts.cli.clear_logs.clear_logs import cli_clear_logs
from scripts.cli.issue.issue import cli_issue
from scripts.cli.remove_template.remove_template import cli_remove_template
from scripts.cli.version.version import cli_version

cli: Typer = typer.Typer(name="nexus-download-flow")


@cli.command()
def version() -> None:
    """Print the current version number of Nexus Download Flow."""
    cli_version()


@cli.command()
def add_templates(paths: List[str]) -> None:
    """
    Add user's custom templates to Nexus Download Flow.

    :param paths: List of template paths to copy
    """
    cli_add_templates(paths)


@cli.command()
def clear_logs() -> None:
    """Clear all content contained in the logs' folder."""
    cli_clear_logs()


@cli.command()
def issue(issue_folder_path: Optional[str] = None) -> None:
    """
    Create an issue file for the user.

    :param issue_folder_path: The path of the folder where the issue file should be created (optional)
    """
    cli_issue(issue_folder_path)


@cli.command()
def remove_template(
    paths: Annotated[List[str] | None, typer.Argument()] = None,
    remove_all: Annotated[bool, typer.Option("--all")] = False,
) -> None:
    """
    Remove user's custom templates from Nexus Download Flow.

    :param paths: List of template paths to remove (optional)
    :param remove_all: A boolean flag to remove all templates included in the templates folder (optional)
    """
    cli_remove_template(paths, remove_all)
