# Clear logs module

Clear logs command module.

## scripts.cli.clear_logs.clear_logs.cli_clear_logs

Clear the logs’ folder.

```python
def cli_clear_logs() -> None:
    print(__STARTING_MESSAGE)
    failed_count: int = 0
    if os.path.exists(LOGS_DIRECTORY):
        for item in os.listdir(LOGS_DIRECTORY):
            item_path: str = os.path.join(LOGS_DIRECTORY, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                failed_count += 1
                setup_logging()
                logging.error(__DELETING_ITEM_ERROR_MESSAGE.format(file_path=item_path, error=e))
                logging_report()
        if failed_count == 0:
            print("The contents of the logs folder have been successfully deleted.")
        else:
            print(f"The contents of the logs folder have been partially deleted. {failed_count} items are remaining.")
    else:
        print("The logs folder do not exist.")
    stop_logging()
```
