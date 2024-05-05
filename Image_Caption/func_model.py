from datetime import datetime
from typing import Any
import logging
from os import path, makedirs


def install_translate_models() -> Any:

    """
    installing the translate model for future usage
    """
    package.install_from_path(path)


def show_progress(done_files: int, start_label: Any, progress_bar: Any) -> None:
    """_summary_
    showing the progress to the user via the tkinter, by updating
    the values
    Args:
        done_files (int): how many files were processed 
        start_label (tk label): showing how many files were processed 
        progress_bar (tk progress bar): the progress bar
    """

    start_label.config(text=str(done_files))

    progress_bar['value'] = done_files



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
    str: the current time
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H-%M")
    return str(formatted_time)


def configure_logger(logger_name: str, log_file: str) -> Any:
    """
    creating a logger file
    :param logger_name str: the name of the logger
    :param log_file str: the name of the logger file
    :return:
    logger: a logger object
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
    Args:
        info_label (Tkinter label): a label which will be updated
        st (time.time()): starting time
        et (time.time()): end time
          
    :return:
    None
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
