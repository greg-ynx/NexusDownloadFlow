# Remove templates module

Remove template command module.

## scripts.cli.remove_templates.remove_templates.cli_remove_templates

Delete custom templates’ directory.

```python
def cli_remove_templates(paths: List[str] | None, remove_all: bool = False) -> None:
    setup_logging()
    try:
        if remove_all:
            __delete_custom_templates_folder()
            return
        if not os.path.exists(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            logging.warning(CUSTOM_TEMPLATES_FOLDER_DOES_NOT_EXIST_WARNING_MESSAGE)
            return
        if paths:
            for path in paths:
                __delete_custom_template_file(path)
        else:
            logging.warning(__PATHS_NO_PATH_GIVEN_WARNING_MESSAGE)
    except NotADirectoryError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        stop_logging()
```
