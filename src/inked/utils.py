from pathlib import Path
from typing import Any, List
from io import BytesIO

import cv2
import numpy as np
import requests
from PIL import Image

AVAILABLE_SIZES = ["lrg", "med", "sml"]
REQUIRED_FILES = ["data.mdb", "lock.mdb", "details.json"]


def random_sample_arr(arr: List[Any], k: int) -> Any:
    """Utility method to find K random array from array of arrays - np.random.choice doesnt work out of the box"""
    return [arr[x] for x in np.random.choice(range(len(arr)), k)]


def random_choice_arr(arr: List[Any]) -> Any:
    """Utility method to find a random array from array of arrays - np.random.choice doesnt work out of the box"""
    return arr[np.random.choice(range(len(arr)))]


def download_charset(size: str) -> None:  # pragma: no cover
    """Downloads lmdb files and details.json for either sml, med or lrg charset images

    Args:
        size (str): One of ["lrg", "med", "sml"]
    """
    assert size in AVAILABLE_SIZES
    folder = Path.home() / ".inked" / size
    folder.mkdir(parents=True, exist_ok=True)
    for file in REQUIRED_FILES:
        if not (folder / file).exists():
            response = requests.get(
                f"https://cg-apac-invent-sva-docclass-data-public.s3-ap-southeast-2.amazonaws.com/inked/charsets/{size}/{file}"
            )
            if response.status_code == 200:
                with open(folder / file, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to download {file}")


def white_to_transparent(img: Image.Image) -> Image.Image:
    """Converts non RGBA images into transparent images by replacing white pixels with alpha

    NOTE: This was faster to convert to numpy than loop over pixel data in Pillow

    Args:
        img (Image.Image): Image to convert

    Returns:
        Image.Image: RGBA image
    """
    if img.mode == "RGBA":
        return img

    img = img.convert("RGBA")
    x = np.asarray(img).copy()
    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)


def darken_greys(image: Image.Image, max: int = 127):
    """Attempts to darken RGB and RGBA images by rescaling color layers from 0-254 to 0-max while keeping 255's constant.
    This is to allow greater separation between pure whites and the rest of the color pallet.

    Args:
        image (np.ndarray): RGB or RGBA image to be color rescaled
        max (int): maximum value to place in RGB layers (rescale 0-254 numbers to 0-max). Does NOT scale 255 values down.

    Returns:
        np.ndarray: Image of same size and shape with color layers values (except 255) scaled.
    """

    reducer = int(255 / max)
    image = np.asarray(image)

    if image.shape[-1] == 4:
        transparency = image[:, :, 3]
        # set transparency to binary
        transparency = np.where(transparency != (0 or 255), 0, transparency)

    img = (np.where(image[:, :, :] != 255, image[:, :, :] / reducer, image[:, :, :])).astype(np.uint8)

    if image.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        img[:, :, 3] = transparency
    return Image.fromarray(img)

def pil_to_bytes(img: Image.Image):
    """Converts an image in memory to bytes object, if it is not already"""
    if isinstance(img, bytes):
        return img
    buffered = BytesIO()
    img.save(buffered, format="png")
    return buffered.getvalue()