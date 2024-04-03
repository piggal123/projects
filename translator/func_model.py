from datetime import datetime
from typing import Any
import logging
import re
from os import path, makedirs


def clean_text(text: str) -> str:
    cleaned_text = text.replace("?", ".")
    cleaned_text = cleaned_text.replace("!", ".")

    return cleaned_text


def split_text(text: str) -> [str]:

    cleaned_text = clean_text(text)
    return [cleaned_text[i:i + 400] for i in range(0, len(cleaned_text), 400)]


def remove_numbers(text: str) -> str:
    # Define a translation table to remove digits
    translation_table = str.maketrans('', '', '0123456789')

    return text.translate(translation_table)


def remove_hebrew(text: str) -> str:
    # Define a regular expression pattern to match Hebrew characters
    hebrew_pattern = re.compile(r'[\u0590-\u05FF]+', re.UNICODE)
    # Replace Hebrew characters with an empty string
    cleaned_text = re.sub(hebrew_pattern, '', text)
    return cleaned_text


def create_folder(folder: str) -> None:
    """
    recreating the folders to clear the data inside
    :param folder: str, path for the folder to be created at
    :return:
    None
    """
    # checking if the folder exists
    if not path.exists(folder):
        makedirs(folder)


def get_current_time() -> str:
    """
    getting the current time
    :return:
    str, the current time
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H-%M")
    return str(formatted_time)


def configure_logger(logger_name: str, log_file: str) -> Any:
    """
    creating a logger file
    :param logger_name: the name of the logger
    :param log_file: the name of the logger file
    :return:
    logger, a logger object
    """
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)  # Set logging level to INFO

    # Create a file handler
    file_handler = logging.FileHandler(log_file)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


def no_more_files(new_tk_vars: Any, st: Any, et: Any) -> None:
    """
    updating the gui to show the process is done and printing
    how much time the process took

    :return:
    bool: True if there are no more files, false otherwise
    """

    new_tk_vars.info_label.config(text="done")

    total_time = et - st

    hours, minutes, seconds = convert_seconds(total_time)
    print("took " + f"{int(hours)} hours, {int(minutes)} minutes, and {seconds:.2f} seconds")


def convert_seconds(seconds: int) -> (str, str, str):
    """
    dividing the seconds to minute and hours to present better
    the time the program ran for
    :param seconds: int, how many seconds the program ran for
    :return:
    hours: string how many hours the program ran for
    minutes: string how many minutes the program ran for
    seconds: string how many seconds the program ran for
    """
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return hours, minutes, seconds


def setting_tk_values(new_tk_vars: Any, i: int, objects_number: int) -> None:
    """
    updating the tk inter variables
    :param new_tk_vars: tkinter class, class that holds the vars
    :param i: int, the number of the loop
    :param objects_number: int, how many objects were pulled
    :return:
    None
    """
    new_tk_vars.start_label.config(text=str(i * 30000))
    new_tk_vars.progress_bar['value'] = i * 30000
    new_tk_vars.progress_bar['maximum'] = objects_number + i * 30000
    new_tk_vars.end_label.config(text=str(objects_number + i * 30000))