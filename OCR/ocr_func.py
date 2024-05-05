from os import remove
import pytesseract
from PIL import Image, ImageFile
from func_model import is_language
from io import BytesIO
from typing import Any
import warnings

pytesseract.pytesseract.tesseract_cmd = path
warnings.catch_warnings()
warnings.simplefilter("ignore")


def rotate_images(img: Image, number: int) -> Image:
    """_summary_
    Rotating the image by 90* everytime
    Args:
        img (Image): the image that being rotated
        number (int): a counter to how many times the image was rotated already

    Returns:
        Image: The rotated image
    """
    try:
        if number == 0:

            angle_rotation = pytesseract.image_to_osd(image=img ,config="-c min_characters_to_try=5"
                                                      ,output_type=pytesseract.Output.DICT)['orientation']

            return img.rotate(angle_rotation ,expand=True)

        else:

            return img.rotate(90*(number) ,expand=True)

    except pytesseract.TesseractError as e:
        print("tesseracterror:", e)
        return img

    except OSError as e:
        print("oserror:", e)
        return img


def rotation_settings(file_path: str, thread_name: str, dpi: int, psm: str, no_rot: Any) -> (str, bool, int):
    """_summary_
    Checks whenever it's the first or second thread calling it,
    then call the iterator function to extract the text
    Args:
        file_path (str): the file path
        thread_name (str): the name of the thread
        dpi (int): which dpi to use
        psm (str): which psm should the ocr use
        no_rot (Any): if the image should be rotated

    Returns:
        (str, bool, int):  the text that was extracted, if text was found, how many times 
        the image was rotated
    """
    counter = 0
   
    found_text = False

    text = " "

    # checking if it's the first iteration
    if thread_name == "first":
  
        image = Image.open(file_path)   

        text, found_text, counter = iterator(image, psm, no_rot)

    # it isn't the first one
    else:

        image = Image.open(file_path)
        saving_name = file_path.split(".")

        # increasing the image's dpi in order to help the pytesseract
        if dpi < 300:

            image.save(saving_name[0] + "1." + saving_name[1], dpi=(300, 300))
        else:
            image.save(saving_name[0] + "1." + saving_name[1], dpi=(dpi + 300, dpi + 300))

        imag = Image.open(saving_name[0] + "1." + saving_name[1])

        text, found_text, counter = iterator(imag, psm, no_rot)

        # deleting the new photo
        try:
            remove(saving_name[0] + "1."  +saving_name[1])

        except:

            print("failed to delete", saving_name[0] + "1." + saving_name[1])

    return text, found_text, counter


   
def iterator(image: str, psm: str, no_rot: Any) -> (str, bool, int):
    """_summary_
    Extracting the text from the image by rotating it and calling
    the is_language function to determinate if the process was successful.
    Rotating the image by calling rotate function, then extracting the text
    until the function is_language returns true or the image is back
    to its original state.
    Args:
        image (str): the path to the image
        psm (str): which psm to use in the ocr
        no_rot (Any): should the image be rotated

    Returns:
       (str, bool, int): the text that was extracted, if text was found, how many times 
        the image was rotated
    """

    counter = 0
    found_text = False
    text = " "

    # checking if the user checked the fast checkbox
    if no_rot == 1:
        image = rotate_images(image, 0)

        text = pytesseract.image_to_string(image, 'heb+eng', config="--psm  " + psm + "--oem 3")

        # checking if the text isn't gibberish or empty
        if is_language(text) and text != "":
            found_text = True

    # the user wants the slow and safe method
    else:

        for k in range(4):

            image = rotate_images(image, k)

            text = pytesseract.image_to_string(image, 'heb+eng', config="--psm  " + psm + "--oem 3")

            # checking if the text isn't gibberish or empty
            if is_language(text) and text != "":
                found_text = True

                break

        counter += 1

        if not found_text:

            for k in range(4):

                image = rotate_images(image, k)

                # checking which mode the user chose. if it's 11, will change to 6
                if psm == "11":

                    text = pytesseract.image_to_string(image, 'heb+eng', config="--psm 6 --oem 3")

                    # the user chose 6, changing to 11
                else:

                    text = pytesseract.image_to_string(image, 'heb+eng', config="--psm 11 --oem 3")

                    # checking if the text isn't gibberish or empty
                if is_language(text) and text != "":
                    found_text = True

                    break

            counter += 1

    return text, found_text, counter


def rotate(file_path: str, image_name: str, dpi: int, psm: str, no_rot: Any) -> (str, bool, int):
    """_summary_
    converting the pdf pages to images, then calling the iterator to extract the text
    Args:
        file_path (str): the path to the file
        image_name (str): the name of the image
        dpi (int): which dpi to use
        psm (str): which psm to use
        no_rot (Any): should it be rotated

    Returns:
        (str, bool, int): the text that was extracted, if text was found, how many times 
        the image was rotated
    """

    counter = 0
    pdf_to_image = []
    try:
        # getting info from the pdf, checking how many pages it has
        info = pdfinfo_from_path(file_path, poppler_path=path)

    except:

        return "pdf corrupted", False, 0
    max_pages = info["Pages"]

    for page in range(1, max_pages + 1, 10):
        pdf_to_image += convert_from_path(file_path, dpi=dpi,
                                          poppler_path=path, first_page=page,
                                          last_page=min(page + 10 - 1, max_pages))


    found_text = False
    final_text = " "
    # iterating through the images, rotating them until the orientation
    # is correct, then extracting the text
    for i in range(len(pdf_to_image)):

        text, found_text, counter = iterator(pdf_to_image[i], psm, no_rot)
        if i % 10 == 0:
            file_name = file_path.split("/")
            print("rotating file", file_name[-1], "page", i)

        final_text += text

    return final_text, found_text, counter



def save_image(response: Any, thread_name: str, artifact_id: str, dpi: int) -> None:
    """
    saving the image as pdf to be able to extract the text out of it
    :param response: the response from relativity
    :param thread_name: the name of the thread
    :param artifact_id: the unique key of the object in relativity
    :param dpi: which dpi to save the file at 
    :return:
    None
    """
  
    img = Image.open(BytesIO(response.content))

    pdf = img.convert('RGB')
    if thread_name == "first":
      
        # saving the picture as pdf
        pdf.save("files//" + artifact_id + ".pdf", 'PDF', resolution=dpi)

    else:

        # checking if the user didn't choose a dpi higher than the default

        if dpi < 300:

            pdf.save("files//" + artifact_id + ".pdf", 'PDF', resolution=300)

        # the user chose a higher dpi, increasing the picture dpi as a result for the second
        # run
        else:
            pdf.save("files//" + artifact_id + ".pdf", 'PDF',
                     resolution=dpi + 300)
