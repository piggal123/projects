from typing import Any
import re
import logging
from datetime import datetime
from os import path, makedirs
from ocr_func import save_image
from file_formats import supported_format_list


def saving_file(response: Any, artifact_id: str, suffix: str, thread_name: str, dpi: int) -> str:
    """_summary_
    saving the file locally 
    Args:
        response (Any): the repsone from relativity
        artifact_id (str): the unique key of the object in relativity
        suffix (str): the ending of the file, which type it is
        thread_name (str): the name of the thread
    Returns:
        str: the file path
    """
    if suffix not in supported_format_list and suffix != "PDF":

        save_image(response, thread_name, artifact_id, dpi)

        file_path = "files//" + artifact_id + ".pdf"

    # the file is in the supported picture format or a pdf
    else:

        file = open("files//" + artifact_id + "." + suffix.lower(), "wb")
        file.write(response.content)
        file.close()

        file_path = "files//" + artifact_id + "." + suffix.lower()

    return file_path



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



def is_language(text) -> bool:
    """
    Tests whenever the text is composed of real letters or
    gibberish


    Parameters
    ----------
    text : string
        The text that was extracted from the image.

    Returns
    -------
    bool
        True if the text is composed of real letters, false otherwise.

    """

    # cleaning the text from non english chars
    cleaned_en_text = re.sub(r'[^a-zA-Z]', ' ', text).lower()

    # cleaning the text from non hebrew chars
    cleaned_he_text = re.sub(r'[a-zA-Z\d|./):~]', ' ', text)
    # Split the text into words
    en_words_list = cleaned_en_text.split()
    heb_words_list = cleaned_he_text.split()

    english_words = ""

    # loading the english words from the file
    with open("words/words.txt", 'r') as file:
        english_words = set(file.read().split())

    hebrew_words = ""

    # loading the hebrew words from the file
    with open("words/hebrew_words.txt", "r", encoding="utf-8") as file:
        hebrew_words = set(file.read().split())

    total_en_words = len(en_words_list)
    total_heb_words = len(heb_words_list)

    # checking if the text from the file is empty
    if (total_en_words == 0 and total_heb_words == 0):

        return True

    else:
        # summing up the amount of non english words
        non_english_words = sum(1 for word in en_words_list if word not in english_words)

        # checking if there aren't any english words
        if total_en_words == 0:

            # setting the ratio so it won't interfere with the result later
            en_gibberish_ratio = 0.6

        else:

            # checking what is the ratio of non english words to the total
            # amount of the words
            en_gibberish_ratio = non_english_words / total_en_words

        # summing up the amount of non hebrew words
        non_hebrew_words = sum(1 for word in heb_words_list if word not in hebrew_words)

        # checking if there aren't any hebrew words
        if total_heb_words == 0:

            # setting the ratio so it won't interfere with the result later
            heb_gibberish_ratio = 0.8

        else:
            # checking what is the ratio of non hebrew words to the total
            # amount of the words
            heb_gibberish_ratio = non_hebrew_words / total_heb_words

    if en_gibberish_ratio < 0.5 or heb_gibberish_ratio < 0.7:

        return True

    else:
        return False


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

