"""Parameters file."""
import logging


def ask_to_keep_logfile() -> bool:
    """
    Ask if the user wants to keep the logfile.

    :return: Whether to keep logfile.
    """
    while True:
        keep: str = str(input("Would you like to save the logfile? (y/n)\n"))
        match keep:
            case "y" | "Y":
                logging.info("Logfile will be saved.")
                return True
            case "n" | "N":
                logging.info("Logfile will be saved only if an exception/error occurred.")
                return False
            case _:
                continue
