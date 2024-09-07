"""All CLI commands of Nexus Download Flow."""

from typing import Annotated, List, Optional

import typer
from typer import Typer

from scripts.cli.add_template.add_templates import cli_add_templates
from scripts.cli.clear_logs.clear_logs import cli_clear_logs
from scripts.cli.issue.issue import cli_issue
from scripts.cli.remove_templates.remove_templates import cli_remove_templates
from scripts.cli.run.run import cli_run
from scripts.cli.run.run_mode_enum import RunModeEnum
from scripts.cli.version.version import cli_version

RUN_MODE_NAME: str = "--mode"
RUN_MODE_SHORT_NAME: str = "-m"
RUN_MODE_HELP: str = "Execution mode for Nexus Download Flow"
RUN_VERSION_SHORTNAME: str = "-v"
RUN_VERSION_HELP: str = "Print the current version number of Nexus Download Flow."
ADD_TEMPLATES_HELP: str = "List of template paths to add to Nexus Download Flow."
ISSUE_ISSUE_FOLDER_PATH_NAME: str = "--folder"
ISSUE_ISSUE_FOLDER_PATH_SHORT_NAME: str = "-f"
ISSUE_ISSUE_FOLDER_PATH_HELP: str = "Path of the folder where the issue file will be stored."
REMOVE_TEMPLATES_PATHS_TEMPLATES_HELP: str = "List of template paths to remove."
REMOVE_TEMPLATES_REMOVE_ALL_TEMPLATES_NAME: str = "--all"
REMOVE_TEMPLATES_REMOVE_ALL_TEMPLATES_SHORT_NAME: str = "-a"
REMOVE_TEMPLATES_REMOVE_ALL_TEMPLATES_HELP: str = "Remove all custom templates from Nexus Download Flow."

cli: Typer = typer.Typer(name="Nexus Download Flow")


@cli.callback(invoke_without_command=True)
def run(ctx: typer.Context,
        mode: Annotated[
            RunModeEnum,
            typer.Option(RUN_MODE_NAME, RUN_MODE_SHORT_NAME, help=RUN_MODE_HELP)
        ] = RunModeEnum.CLASSIC,
        _version: Annotated[
            bool,
            typer.Option(RUN_VERSION_SHORTNAME, help=RUN_VERSION_HELP)
        ] = False) -> None:
    """
    Run the auto downloader.

    :param _version: Version option
    :param ctx: Context for exclusive executable callback
    :param mode: Mode to launch_ndf the auto downloader (optional)
    """
    if _version:
        cli_version()
        return

    if ctx.invoked_subcommand is None:
        cli_run(mode)


@cli.command()
def version() -> None:
    """Print the current version number of Nexus Download Flow."""
    cli_version()


@cli.command()
def add_templates(paths: Annotated[
    List[str],
    typer.Argument(help=ADD_TEMPLATES_HELP)
]) -> None:
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
def issue(issue_folder_path: Annotated[
    Optional[str],
    typer.Option(
        ISSUE_ISSUE_FOLDER_PATH_NAME,
        ISSUE_ISSUE_FOLDER_PATH_SHORT_NAME,
        help=ISSUE_ISSUE_FOLDER_PATH_HELP
    )
] = None) -> None:
    """
    Create an issue file for the user.

    :param issue_folder_path: The path of the folder where the issue file should be created (optional)
    """
    cli_issue(issue_folder_path)


@cli.command()
def remove_templates(
    paths: Annotated[List[str] | None, typer.Argument(help=REMOVE_TEMPLATES_PATHS_TEMPLATES_HELP)] = None,
    remove_all: Annotated[
        bool,
        typer.Option(
            REMOVE_TEMPLATES_REMOVE_ALL_TEMPLATES_NAME,
            REMOVE_TEMPLATES_REMOVE_ALL_TEMPLATES_SHORT_NAME,
            help=REMOVE_TEMPLATES_REMOVE_ALL_TEMPLATES_HELP
        )] = False,
) -> None:
    """
    Remove user's custom templates from Nexus Download Flow.

    :param paths: List of template paths to remove (optional)
    :param remove_all: A boolean flag to remove all templates included in the templates folder (optional)
    """
    cli_remove_templates(paths, remove_all)
