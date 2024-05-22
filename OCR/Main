from tkinter import Button, Tk
import classes
import func_model
from typing import Any
import warnings
from threading import Lock, Thread
from multiprocessing.pool import ThreadPool
import server_model
from relativity_settings import head
import time
from os import environ, remove, path
import ocr_func

all_objects = []
func_model.create_folder("logs//")
logger = func_model.configure_logger('my_logger',  "logs//" + func_model.get_current_time() + ".log")
lock = Lock()
environ['CURL_CA_BUNDLE'] = ''
st = time.time()
gui_vars = classes.GuiVars(st)
errors_class = classes.ErrorsWriter(func_model.get_current_time(), "errors//")
stop_flag = False



def add_to_list(workspace_id: str, thread_name: str) -> None:
    """
    calling the pull request until there are none more objects
    to pull
    :param workspace_id str: the unique key of the case in relativity
    :return: None
    """
    i = 0
    while not stop_flag:
        
        data = server_model.pull_request(workspace_id, i, head, thread_name)
       
        all_objects.append(data)

        i += 1
        if not data:

            break


class MyThread(Thread):
    def __init__(self, name, new_tk_vars: classes.TkVars, second_thread: Any):
        Thread.__init__(self)
        self.name = name
        self.new_tk_vars = new_tk_vars
        self.second_thread = second_thread

    def run(self):

        checker(self.new_tk_vars, self.name, self.second_thread)


def start(tk_vars: classes.TkVars) -> None:
    """
    Starting the code in a different thread so the gui won't freeze
    args:
        tk_vars TkVars: a class instance that holds the tkinter info
    :return:
    None
    """
    second_run_thread = MyThread("second", tk_vars, " ")
    first_run_thread = MyThread("first", tk_vars, second_run_thread)

    first_run_thread.start()


def info_download(tk_vars: classes.TkVars, objects: [str], i: int, thread_name: str) -> None:
    """
    Updating the gui variables and calling the translate function
    :param tk_vars classes.TkVars: a class instance that holds the tkinter info
    :param objects [str]: list of objects from relativity
    :param objects: list of objects from relativity
    :param i: int, the number of the run
    :return:
    None
    """
    

    tk_vars.info_label.config(text=thread_name + " run in progress")

    func_model.setting_tk_values(tk_vars, i, len(objects))


    # checking if the threads check box was checked
    if tk_vars.no_thread_check_box.get() == 1:

        files_download(tk_vars, objects, thread_name, False)

    else:
        pool = ThreadPool(processes=gui_vars.workers)
        threads = []
        chunk_iterator = classes.ChunkIterator(objects, gui_vars.workers)

        for partial_objects_list in chunk_iterator:
            threads.append(pool.apply_async(files_download, (tk_vars, partial_objects_list, thread_name, True)))

        for thread in threads:
            thread.get()

        pool.close()
        pool.join()

def files_download(tk_vars: classes.TkVars, partial_objects_list: [str], thread_name: str, lock_required: bool) -> None:
    """
    Download the files and saving them locally after checking if they are in the
    supported formats while updating the tkinter variables during the process

    Args:
        tk_vars (classes.TkVars):  a class instance that holds the tkinter info
        partial_objects_list ([str]): objects list from relativity
        thread_name (str): the name of the thread
        lock_required (bool): checker if threads are being used or just a single one
    """

    tk_vars.info_label.config(text=thread_name + " ocr in progress")

    iterator = classes.StringListIterator(partial_objects_list)

    for string in iterator:

        if 'ArtifactID' in string:
            artifact_id = str(string['ArtifactID'])
            try:

                try:
                    if thread_name == "second" and string['FieldValues'][1]["Value"] != "failed to find text":
                        gui_vars.done_files += 1
                        continue

                except:
                    pass

                suffix = string['FieldValues'][0]["Value"]
                response = server_model.download_file_request(gui_vars.workspace_id, artifact_id, head)

                if not response:

                    continue

                file_path = func_model.saving_file(response, artifact_id, suffix, thread_name, tk_vars.dpi)
          
                extract_text(file_path, suffix, thread_name, tk_vars.dpi, tk_vars.psm, tk_vars.no_rot, artifact_id)

            except Exception as e:

                logger.error("An exception occurred " + artifact_id, exc_info=True)

                print("error is", e)

                text = "updated to relativity, failed to save "
                
                errors_class.saving_excel(artifact_id, text)

                if server_model.push_request(text, artifact_id, gui_vars.workspace_id, head, False):
                    print(text + artifact_id)

        gui_vars.done_files += 1

        if lock_required:
            # making sure the theards won't access the same variable at the same time
            with lock:
                func_model.show_progress(gui_vars.done_files, tk_vars.start_label, tk_vars.progress_bar)

        else:
            func_model.show_progress(gui_vars.done_files, tk_vars.start_label, tk_vars.progress_bar)


def extract_text(file_path: str, suffix: str, thread_name: str, dpi: int, psm: str, no_rot: Any, artifact_id: str) -> None:
    """_summary_
    extracting the text by calling the methods, then sending a push request to relativity
    Args:
        file_path (str): the file path
        suffix (str): the ending of the file
        thread_name (str): the thread name
        dpi (int): which dpi the image is 
        psm (str): which psm ocr should use
        no_rot (Any): should the image be rotated
        artifact_id (str): the unique key of the object in relativity
    """

    try:
        # checking if the file is pdf

        if suffix == "PDF":
          
            # extracting the text with rotate method
            text, success, counter = ocr_func.rotate(file_path, artifact_id, dpi, psm, no_rot)

        # it's not a pdf, means it's a single image
        else:
           
            text, success, counter = ocr_func.rotation_settings(file_path, thread_name, dpi, psm, no_rot)

        if success and text != "":
           
            if server_model.push_request(text, artifact_id, gui_vars.workspace_id, head, True):
                print("file {} was successfully uploaded to Relativity".format(artifact_id))
           
        else:
            
            text = "failed to find text"

            if server_model.push_request(text, artifact_id, gui_vars.workspace_id, head, False):
                print("{} failed to find text".format(artifact_id))
             
    # the extraction failed
    except Exception as e:

        text = "tesseract failed " + str(e)
        logger.error("An exception occurred " + artifact_id, exc_info=True)
        if server_model.push_request(text, artifact_id, gui_vars.workspace_id, head, False):
         
            print("file {}".format(artifact_id), text)

    # deleting the file once we are done with it
    remove(file_path)


def loop_start(tk_vars: classes.TkVars, thread_name: str) -> None:
    """_summary_
    starting the loop to iterate through the objects from relativity
    Args:
        tk_vars (classes.TkVars): a class instance that holds the tkinter info

    Returns:
        None
    """
    for i in range(50000):

        if i == 0:

            start_loop_time_tracker = time.time()
            
            # waiting for the response from relativity
            while True:
                
                try:

                    partial_objects_list = all_objects[i]

                    # we got a response, the list isn't empty, break the loop
                    if len(partial_objects_list) > 0:
                        
                        info_download(tk_vars, partial_objects_list, i, thread_name)
                        break
                
                    # too much time went by, user didn't mark anything in relativity
                    if func_model.run_time_checker(start_loop_time_tracker):
                        print("did you mark the right conditions in relativity?")
                        break
                    
                except Exception as e:
                    if func_model.run_time_checker(start_loop_time_tracker):
                        print("error is", e)
                        logger.error("An exception occurred " , exc_info=True)
                        break
                    pass
                time.sleep(1)

        # not the first iteration, no need to wait anymore for response        
        else:
            # checking if there are objects to itreate through or we done
            try:
                partial_objects_list = all_objects[i]

                if len(partial_objects_list) > 0:
                    
                    info_download(tk_vars, partial_objects_list, i, thread_name)

            except:

                et = time.time()
                func_model.no_more_files(tk_vars.info_label, gui_vars.st, et)
                stop_flag = True
                background_thread.join()
                break


def checker(tk_vars: classes.TkVars, thread_name: str, second_thread: MyThread) -> None:
    """_summary_
    checking if the user's inputs are legal
    Args:
        tk_vars (classes.TkVars): a class instance that holds the tkinter info
        thread_name (str): the thread's name
        second_thread (MyThread): the second thread
    """

    workspace_id = tk_vars.workspace_id_entry.get()

    if workspace_id == "":

        tk_vars.workspace_error_label.config(text="ENTER CASE ID", fg="red")

    else:
        tk_vars.workspace_error_label.config(text="V", fg="green")

        gui_vars.workspace_id = workspace_id

        warnings.catch_warnings()
        warnings.simplefilter("ignore")
        try:
            gui_vars.workers = int(tk_vars.workers.get())

        except:
            gui_vars.workers = 16

        try:
            tk_vars.dpi = int(tk_vars.dpi_entry.get())

        # if the user didn't input any, will set it to 100
        except:

            if thread_name == "first":

                tk_vars.dpi = 100

            # increasing the dpi for the second run if the user didn't choose a dpi
            else:

                tk_vars.dpi = 300

        tk_vars.psm = str(tk_vars.psm_entry.get())

        func_model.create_folder("errors//")
        func_model.create_folder("files//")

        tk_vars.info_label.config(text="waiting for response")

        background_thread = Thread(target=lambda: add_to_list(workspace_id, thread_name))

        # Start the thread
        background_thread.start()

        if thread_name == "second":
            print("here")
            all_objects.clear()

        loop_start(tk_vars, thread_name)

        if thread_name == "first" and tk_vars.no_rot.get() == 0:
          
            second_thread.start()


def gui_configuration() -> None:
    """
    creating a TkVars instance to generate the tkinter view
    :return:
    None
    """
    font_tuple = ("Comic Sans MS", 20, "bold")
    font_size = 14

    tk_vars = classes.TkVars(window, font_size, font_tuple)

    start_button = Button(text="start", font=font_size,
                          command=lambda: start(tk_vars))
    start_button.grid(row=15, column=2)

    window.focus()
    window.mainloop()


if __name__ == "__main__":
    window = Tk()
    window.geometry('380x400')

    gui_configuration()
