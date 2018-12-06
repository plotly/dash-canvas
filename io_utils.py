from PIL import Image
from io import BytesIO
import base64


def image_string_to_PILImage(image_string):
    """
    Converts image string to PIL image object.
    """
    return Image.open(BytesIO(base64.b64decode(image_string[22:])))
