from tkinter.ttk import Progressbar
from tkinter import IntVar, Checkbutton, Label, Entry, HORIZONTAL, StringVar, OptionMenu
import pandas as pd
from typing import Any


class ResultsDf:
    def __init__(self):
        self.final_df = pd.DataFrame(
            columns=["Control Number", "Custodian", "file name", "File Extension", "Native File", "Group Identifier",
                     "Investigator Notes"])

    def saving_csv(self, current_time: Any):
        self.final_df.to_csv("excel//upload " + current_time + ".csv", index=False)

    def adding_row(self, converted_file_path, custodian, control_number):
        converted_file_name = converted_file_path.split("//")[-1]
        converted_suffix = converted_file_path.split(".")[-1]
        converted_control_number = control_number + "_0001"
        text = "Created by ICA for imaging purpose"
        converted_file_df = pd.DataFrame({"Control Number": [converted_control_number], "Custodian": [custodian],
                                          "File Extension": [converted_suffix.upper()],
                                          "file name": [converted_file_name], "Native File": [converted_file_path]
                                             , "Group Identifier": [control_number], "Investigator Notes": [text]})

        self.final_df = pd.concat([self.final_df, converted_file_df], ignore_index=True, axis=0)


class TkVars:
    folder_path = ""

    def __init__(self, window, font_text, font_tuple):
        """
        :param window:
        :param font_text:
        :param font_tuple:

        returns:

        """
        self.window = window
        self.no_thread_check_box = IntVar()

        title = Label(text="CONVERTOR")
        title.configure(font=font_tuple)
        title.grid(row=0, column=2)

        label_one = Label(text="choose a folder to load from", font=font_text)
        label_one.grid(row=1, column=2)

        label_two = Label(text="then press start", font=font_text)
        label_two.grid(row=2, column=2)

        case_id_label = Label(self.window, text="CaseID", font=font_text)
        case_id_label.place(x=50, y=90)

        self.workspace_error_label = Label(self.window, text=" ", font=font_text)
        self.workspace_error_label.place(x=280, y=90)

        self.workspace_id_entry = Entry(self.window)
        self.workspace_id_entry.grid(row=3, column=2)

        self.info_label = Label(text="", font=font_text, width=42)
        self.info_label.grid(row=4, column=2)

        self.start_label = Label(text="", font=font_text)
        self.start_label.place(x=75, y=133)

        self.progress_bar = Progressbar(self.window, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.grid(row=5, column=2)

        self.end_label = Label(text=" ", font=font_text)
        self.end_label.place(x=255, y=133)

        self.thread_button = Checkbutton(text="no threads", variable=self.no_thread_check_box, font=font_text)
        self.thread_button.grid(row=6, column=2)

        workers_options = []

        for i in range(1, 9):
            workers_options.append(str(i))

        self.workers = StringVar(self.window)
        self.workers.set("Select Threads")

        workers_menu = OptionMenu(self.window, self.workers, *workers_options)
        workers_menu.grid(row=7, column=2)

        folder_error_label = Label(text="", font=font_text)
        folder_error_label.place(x=255, y=210)


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
