from requests import post, get
from typing import Any


def push_request(artifact_id: str, workspace_id: str, head: {str, str}, text: str) -> bool:
    """
    sending a push request to relativity to update the relevant fields
    Args:
        text (str): the translated text 
        artifact_id (str): the unique key of the object in relativity
        workspace_id (str): the unique key of the case in relativity
        head (str, str): the required headers to access relativity

    Returns:
        bool: true if the update was successful, false otherwise
    """
    update_body = {
        "Request": {
            "Object": {
                "ArtifactID": artifact_id
            },
            "FieldValues": [
                {
                    "Field": {
                        "Name": "field_name"
                    },
                    "Value": text
                },
                {
                    "Field": {
                        "Name": "field_name"
                    },

                    "Value": False
                },

            ]
        }
    }
    response = post(url=
                             'https://relativity-web/Relativity.Rest/API/Relativity.Objects/workspace/' + workspace_id + '/object/update',
                             json=update_body, headers=head, verify=False)
    if response.ok:
        return True
    else:
        print("ERROR:", artifact_id)
        return False


def download_file_request(workspace_id: str, artifact_id: str,  head: {str, str}) -> Any:
    """
    sending a get request to download the file from relativity
    Args:
        workspace_id (str):  the unique key of the case in relativity
        artifact_id (str):  the unique key of the object in relativity
        head (str, str): the required headers to access relativity

    Returns:
        Any: the repsonse from relativity
    """

    response = get(url='https://relativity-web/Relativity.Rest/API/Relativity.Document/workspace/' +
                       workspace_id + '/downloadnativefile/' + artifact_id, headers=head, verify=False)

    if response.status_code != 200:

        # checking what is the response error text
        try:
            # getting the text
            text = response.text.split(":")
            error_code_text = text[3].replace("}", "")
            error_code_text = error_code_text.replace('"', '')
            error_code_text = error_code_text + " error code: " + str(response.status_code)

        # failed to get the error text
        except:
            error_code_text = "error code: " + str(response.status_code)

        print("error code is", error_code_text)
        return False

    return response


def pull_request(workspace_id: str, i: int, head: {str, str}) -> [str]:

    """
    creating pull request to relativity to get the objects from the server
    :param workspace_id str: the unique key of the case in relativity
    :param head {str,str}:  the required headers to access relativity
    :param i int: which loop number it is
    :return:
    str: the response from relativity
    """

    request_body = {
        "Request": {
            "ObjectType": {
                "ArtifactTypeID": 10
            },
            "fields": [
                {"Name": "File Extension"},

            ],
            "condition": "'field_name' == True",
            "sorts": [
            ]
        },

        "start": i * 30000,
        "length": 30000
    }

    response = post(url='https://relativity-web/Relativity.Rest/API/Relativity.Objects/workspace/' +
                                 workspace_id + '/object/query',
                             json=request_body, headers=head, verify=False)

    data = response.json()['Objects']

    return data


def clean_error_text(response: Any, logger: Any) -> None:
    """
    extracting the error text out of the response from relativity server
    :param response: the response from relativity
    :param logger: logging object
    :return:
    str: the cleaned error text
    """
    try:

        text = response.text.split(":")
        error_code_text = text[3].replace("}", "")
        error_code_text = error_code_text.replace('"', '')
        error_code_text = error_code_text + " error code: " + str(response.status_code)

    # failed to get the error text
    except:
        logger.error("An exception occurred", exc_info=True)
        error_code_text = "error code: " + str(response.status_code)

    print(error_code_text)
