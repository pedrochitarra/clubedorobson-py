"""Functions to get information about images."""
import base64
import requests


def create_blob_from_file(file_path: str):
    """In markdown HTML at Streamlit, we can't use the src attribute of an
    image tag to show an image from a file path. So, we need to convert the
    image to a blob and then use the src attribute of the image tag to show
    the image."""
    # Check if the image is local or remote
    if file_path.startswith("http"):
        response = requests.get(file_path)
        contents = response.content
    else:
        file = open(file_path, "rb")
        contents = file.read()
        file.close()
    file_blob = base64.b64encode(contents).decode("utf-8")

    return file_blob
