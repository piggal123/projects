import pandas as pd
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import IntVar, Checkbutton
from typing import Any


class TkVars:

    def __init__(self, window: Any, font_size: int, font_tuple: (str, int, str)) -> None:
        """
        setting the tkvars class
        Args:
            window (tkinter window): the window of tkinter
            font_size (int): the size of the funt
            font_tuple (str, int, str): which font, size of it and setting it to bold of the header
        """
        self.window = window
        self.no_thread_check_box = IntVar()
        self.no_rot = IntVar()

        title = tk.Label(text="OCR")
        title.configure(font=font_tuple)
        title.grid(row=0, column=2)

        label_one = tk.Label(text="choose a folder to load from", font=font_size)
        label_one.grid(row=1, column=2)

        label_two = tk.Label(text="then press start", font=font_size)
        label_two.grid(row=2, column=2)

        case_id_label = tk.Label(self.window, text="CaseID", font=font_size)
        case_id_label.place(x=50, y=90)

        self.workspace_error_label = tk.Label(self.window, text=" ", font=font_size)
        self.workspace_error_label.place(x=260, y=90)

        self.workspace_id_entry = tk.Entry(self.window)
        self.workspace_id_entry.grid(row=3, column=2)

        self.info_label = tk.Label(text="", font=font_size, width=42)
        self.info_label.grid(row=4, column=2)

        self.start_label = tk.Label(text="", font=font_size)
        self.start_label.place(x=75, y=133)

        self.progress_bar = Progressbar(self.window, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.grid(row=5, column=2)

        self.end_label = tk.Label(text=" ", font=font_size)
        self.end_label.place(x=255, y=133)

        self.thread_button = Checkbutton(text="no threads", variable=self.no_thread_check_box, font=font_size)
        self.thread_button.grid(row=6, column=2)

        workers_options = []

        for i in range(1, 9):
            workers_options.append(str(i))

        self.workers = tk.StringVar(self.window)
        self.workers.set(workers_options[7])

        workers_menu = tk.OptionMenu(window, self.workers, *workers_options)
        workers_menu.grid(row=7, column=2)

        dpi_label = tk.Label(text="dpi", font=font_size)
        dpi_label.place(x=140, y=225)

        self.dpi_entry = tk.Entry(window, width=4)
        self.dpi_entry.grid(row=8, column=2, pady=10)

        self.dpi = 100

        self.fast_button = Checkbutton(text="fast", variable=self.no_rot, font=font_size)
        self.fast_button.grid(row=9, column=2)

        psm_label = tk.Label(text="psm mode", font=font_size)
        psm_label.place(x=75, y=285)

        psm_options = ["6", "11"]
        self.psm_entry = tk.IntVar(self.window)
        self.psm_entry.set(psm_options[0])

        self.psm = "6"

        psm_menu = tk.OptionMenu(window, self.psm_entry, *psm_options)
        psm_menu.grid(row=10, column=2)


class ErrorsWriter:

    def __init__(self, file_name: str, error_path: str):

        self.file_name = file_name
        self.error_df = pd.DataFrame(columns=["artifact ID", "error"])
        self.error_path = error_path


    def empty_excel(self) -> None:
        """
        checking whenever the Excel is empty. if so, saving it with no error were found
        :return:
        None
        """
        if self.error_df.empty:
            self.saving_excel("no errors", "were found")


    def saving_excel(self, artifact_id: str, error: str) -> None:

        """
        updating the Excel with the file name and error, then saving it
        :param artifact_id: str, the artifact id of the object
        :param error: str, which error occurred
        :return:
        None
        """
        # creating a row with the file name and the error
        error_row = pd.DataFrame([{'artifact ID': artifact_id, 'error': error}])

        # concatenating the row with the pandas
        self.error_df = pd.concat([self.error_df, error_row])

        # creating a writer for the Excel
        writer = pd.ExcelWriter(self.error_path + self.file_name + ".xlsx", engine='xlsxwriter')

        self.error_df.to_excel(writer, sheet_name="errors", index=False)
        worksheet = writer.sheets["errors"]
        worksheet.set_column(0, 2, 30)

        # saving the Excel
        writer.close()


class StringListIterator:

    def __init__(self, string_list):
        self.string_list = string_list
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.string_list):
            result = self.string_list[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


class ChunkIterator:

    def __init__(self, all_objects, num_chunks):
        self.all_objects = all_objects
        self.num_chunks = num_chunks
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.num_chunks:
            start_index = self.index
            result = self.all_objects[start_index::self.num_chunks]
            self.index += 1
            return result
        else:
            raise StopIteration


class GuiVars:

    def __init__(self, st: Any):

        self.workspace_id = ""

        self.st = st
        self.workers = 6
        self.done_files = 0
