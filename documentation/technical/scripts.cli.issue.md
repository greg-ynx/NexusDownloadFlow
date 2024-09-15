# Issue module

Issue file generator command module.

## scripts.cli.issue.issue.cli_issue

Create the issue text file to copy/paste to our repository on GitHub.

```python
def cli_issue(issue_folder_path: str | None = None) -> None:
    setup_logging()
    logging.info(__STARTING_MESSAGE)
    try:
        output_file_path: str = __get_issue_file_path(issue_folder_path)

        issue_title: str = typer.prompt("Please enter a title for your issue")
        issue_description: str = typer.prompt("Please describe your issue")
        system_info: dict[str, str] = __get_user_system_info()
        ndf_version: str = PROJECT_VERSION

        filled_issue_content: str = __fill_issue_template(
            issue_title=issue_title, ndf_version=ndf_version, issue_description=issue_description, **system_info
        )

        __write_issue_file(output_file_path, filled_issue_content)
        print(filled_issue_content)
        logging.info(__SUCCESS_MESSAGE)
    except FileNotFoundError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        stop_logging()
```
