# Add templates module

Add template command module.

## scripts.cli.add_template.add_templates.cli_add_templates

Add custom templates.

* **Parameters:**
  **paths** – Path list of the templates.

```python
def cli_add_templates(paths) -> None:
    setup_logging()
    try:
        logging.info(__CLI_ADD_TEMPLATES_START_MESSAGE)
        __check_paths(paths)

        for path in paths:
            __verify_image(path)

        if not os.path.exists(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            os.makedirs(CUSTOM_TEMPLATES_DIRECTORY_PATH)
        elif not os.path.isdir(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            raise NotADirectoryError(CUSTOM_TEMPLATES_DIRECTORY_IS_NOT_A_DIRECTORY_ERROR_MESSAGE)

        for path in paths:
            file_path: str = shutil.copy(path, CUSTOM_TEMPLATES_DIRECTORY_PATH)
            logging.info(__CLI_ADD_TEMPLATES_SUCCESS_MESSAGE.format(file_path=file_path))

    except ValueError as e:
        logging.error(e)
    except NotADirectoryError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        stop_logging()
```
