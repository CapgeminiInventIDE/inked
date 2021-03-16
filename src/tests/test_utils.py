import io
import numpy as np
import pytest
from PIL import Image
from pathlib import Path

from ..inked.utils import white_to_transparent, pil_to_bytes

ALL_WHITE = np.ones((3, 3, 3), dtype=np.uint8) * 255

PARTIAL_TRANSPARENT = np.array(
    [
        [[255, 255, 255, 0], [255, 255, 255, 255], [255, 255, 255, 255]],
        [[255, 255, 255, 0], [255, 255, 255, 255], [255, 255, 255, 255]],
        [[255, 255, 255, 0], [255, 255, 255, 255], [255, 255, 255, 255]],
    ],
    dtype=np.uint8,
)

ALL_TRANSPARENT = np.array(
    [
        [[255, 255, 255, 0], [255, 255, 255, 0], [255, 255, 255, 0]],
        [[255, 255, 255, 0], [255, 255, 255, 0], [255, 255, 255, 0]],
        [[255, 255, 255, 0], [255, 255, 255, 0], [255, 255, 255, 0]],
    ],
    dtype=np.uint8,
)

ALL_WHITE_GREYSCALE = np.ones((3, 3, 1), dtype=np.uint8)[0] * 255


@pytest.mark.parametrize(
    "incoming, expected",
    [
        (ALL_WHITE, ALL_TRANSPARENT),  # Test that when we load image that is all white -> all transparent
        (ALL_TRANSPARENT, ALL_TRANSPARENT),  # Test that when we load image that is all transparent -> all transparent
        (  # Test that when we load image that is partial transparent -> partial transparent
            PARTIAL_TRANSPARENT,
            PARTIAL_TRANSPARENT,
        ),
        (  # Test that when we load image that is all white greyscale -> all transparent
            ALL_WHITE_GREYSCALE,
            ALL_TRANSPARENT,
        ),
    ],
)
def test_white_to_transparent(incoming, expected):
    incoming = Image.fromarray(incoming)
    assert np.equal(np.array(white_to_transparent(incoming)), expected).all()


def test_pil_to_bytes():
    pil_img = Image.open(str(Path(__file__).parent / "data" / "demo.png")).convert("RGBA")
    bytes_img = pil_to_bytes(pil_img)
    # check image hasn't changed
    assert np.array(Image.open(io.BytesIO(bytes_img)).convert("RGBA")).all() == np.array(pil_img).all()
    # check early return
    assert bytes_img == pil_to_bytes(bytes_img)