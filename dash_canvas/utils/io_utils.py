from PIL import Image
from io import BytesIO
import base64

_allowed_formats = {
    "jpg",
    "png",
    "tiff",
}

def array_to_data_url(img, dtype=None, format="png"):
    """
    Converts numpy array to data string, using Pillow.

    The returned image string has the right format for the ``image_content``
    property of DashCanvas.

    Parameters
    ==========

    img : numpy array
    dtype : numpy datatype
    format : Optional str, one of "jpg", "png" (default), or "tiff"

    Returns
    =======

    image_string: str
    """
    if dtype is not None:
        img = img.astype(dtype)
    if not format in _allowed_formats:
        format = "png"
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format=format)
    prefix = 'data:image/' + format + ';base64,'
    image_string = prefix + base64.b64encode(buff.getvalue()).decode("utf-8")
    return image_string


def image_string_to_PILImage(image_string):
    """
    Converts image string to PIL image object.
    """
    return Image.open(BytesIO(base64.b64decode(image_string[22:])))
