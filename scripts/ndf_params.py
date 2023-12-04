"""Parameters file."""
import logging

__KEEP: str = str(input("Would you like to save the logfile? (y/n)\n"))


def ask_to_keep_logfile() -> bool:
    """
    Ask if the user wants to keep the log file.

    :return: Bool value representing whether to keep the log file or not.
    True, if user's answer is "y" or "Y".
    False, if user's answer is "n" or "N".
    Will repeat if the input value is not valid.
    """
    while True:
        match __KEEP:
            case "y" | "Y":
                logging.info("Logfile will be saved.")
                return True
            case "n" | "N":
                logging.info("Logfile will be saved only if an exception/error occurred.")
                return False
            case _:
                continue
