import requests
import logging
import os
import base64
from PIL import Image

from . import flyer

def get_images(
        url="",
        prompt="puppy dog",
        img_size=(512, 512),
        batch_size=5,
        timeout=30) -> list:
    """
    If size is larger than 720, the model will have strong issues generating good images. 

    A possible workaround is to generate them in a smaller resolution keeping the ratio,
    then use a scaling technique using the API to get the thing at the request resolution.
    """
    if url is None or url == "":
        logging.error("Cannot get images: No Stable Diffusion endpoint defined.")
        return []

    payload = {
      "prompt": prompt,
      "width": img_size[flyer.Flyer.WIDTH],
      "height": img_size[flyer.Flyer.HEIGH],
      "batch_size": batch_size,
    }
    response = None

    try:
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', timeout=timeout, json=payload)
    except Exception as e:
        logging.error(e)
        return []

    if response == None or response.status_code != 200:
        if response != None:
            logging.error(f"Could not fetch response: {response.status_code}")
            logging.debug(response)
        return []
    
    r = response.json()

    images = []
    for image_data in r['images']:
        tmp_file = "/tmp/{os.getpid()}_out.png"
        try:
            os.remove(tmp_file)
        except Exception as e:
            # Nothing to remove
            pass

        # An ugly hack to convert bytes to Pil.Image's
        with open(tmp_file, "wb") as f:
            f.write(base64.b64decode(image_data))
        with Image.open(tmp_file).convert("RGBA") as image:
            images.append(image)
        os.remove(tmp_file)
    return images
