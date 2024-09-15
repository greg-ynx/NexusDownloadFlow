# Commands module

All CLI commands of Nexus Download Flow.

## scripts.cli.commands.add_templates

Add user’s custom templates to Nexus Download Flow.

* **Parameters:**
  **paths** – List of template paths to copy

```python
@cli.command()
def add_templates(paths) -> None:
    cli_add_templates(paths)
```

## scripts.cli.commands.clear_logs

Clear all content contained in the logs’ folder.

```python
@cli.command()
def clear_logs() -> None:
    cli_clear_logs()
```

## scripts.cli.commands.issue

Create an issue file for the user.

* **Parameters:**
  **issue_folder_path** – The path of the folder where the issue file should be created (optional)

```python
@cli.command()
def issue(issue_folder_path = None) -> None:
    cli_issue(issue_folder_path)
```

## scripts.cli.commands.remove_templates

Remove user’s custom templates from Nexus Download Flow.

* **Parameters:**
  * **paths** – List of template paths to remove (optional)
  * **remove_all** – A boolean flag to remove all templates included in the templates folder (optional)

```python
@cli.command()
def remove_templates(paths = None, remove_all = False) -> None:
    cli_remove_templates(paths, remove_all)
```

## scripts.cli.commands.run

Run the auto downloader.

* **Parameters:**
  * **\_version** – Version option
  * **ctx** – Context for exclusive executable callback
  * **mode** – Mode to launch_ndf the auto downloader (optional)

```python
@cli.callback(invoke_without_command=True)
def run(ctx: typer.Context, mode = RunModeEnum.CLASSIC, _version = False) -> None:
    if _version:
        cli_version()
        return

    if ctx.invoked_subcommand is None:
        cli_run(mode)
```

## scripts.cli.commands.version

Print the current version number of Nexus Download Flow.

```python
@cli.command()
def version() -> None:
    cli_version()
```