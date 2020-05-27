from PIL import Image
from io import BytesIO
import base64


def array_to_data_url(img, dtype=None, img_format='png'):
    """
    Converts numpy array to data string, using Pillow.

    The returned image string has the right format for the ``image_content``
    property of DashCanvas.

    Parameters
    ==========

    img : numpy array

    Returns
    =======

    image_string: str
    """
    if dtype is not None:
        img = img.astype(dtype)
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format=img_format)
    if img_format == 'png':
        prefix = b'data:image/png;base64,'
    elif img_format == 'jpeg':
        prefix = b'data:image/jpeg;base64,'
    else:
        raise ValueError("accepted image formats are 'png' and 'jpeg' but %s was passed" %format)
    image_string = (prefix + base64.b64encode(buff.getvalue())).decode("utf-8")
    return image_string


def image_string_to_PILImage(image_string):
    """
    Converts image string to PIL image object.
    """
    if 'png' in image_string[:22]:
        return Image.open(BytesIO(base64.b64decode(image_string[22:])))
    elif 'jpeg' in image_string[:23]:
        return Image.open(BytesIO(base64.b64decode(image_string[23:])))
    else:
        raise ValueError("image string format not recognized")
