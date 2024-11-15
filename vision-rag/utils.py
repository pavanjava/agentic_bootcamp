import base64
from io import BytesIO
from PIL import Image


def decode_base64_image(base64_image_str):
    # Strip the prefix (e.g., 'data:image/jpeg;base64,')
    base64_data = base64_image_str.split(",")[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    return image
