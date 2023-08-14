"""Functions to get information about images."""
import base64


def create_blob_from_file(file_path: str):
    """In markdown HTML at Streamlit, we can't use the src attribute of an
    image tag to show an image from a file path. So, we need to convert the
    image to a blob and then use the src attribute of the image tag to show
    the image."""
    file = open(file_path, "rb")
    contents = file.read()
    file_blob = base64.b64encode(contents).decode("utf-8")
    file.close()

    return file_blob
