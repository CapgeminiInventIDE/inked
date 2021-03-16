import io
import json
from pathlib import Path, PurePath
from typing import Dict, List, Optional, Tuple, Union

import cv2
import lmdb
import numpy as np
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from .augmentor import Augmentor
from .character import Character, FixedSpacer, RandomSpacer, Word
from .scribe import Scribe
from .utils import darken_greys, download_charset, random_choice_arr, white_to_transparent


class CharacterUnavailableError(Exception):
    """Raised when the character requested is not a member of the possible characters to generate"""


class CharacterGenerator(object):
    """Generates fixed or random characters from font files and MNIST style character images"""

    def __init__(
        self,
        warehouses: List[str] = ["fonts"],
        augmentor: Optional[Augmentor] = None,
        font_blacklist: List[str] = [],
        block_dataset_size: str = "sml",
    ):
        assert block_dataset_size in ["sml", "med", "lrg"]

        self.block_dataset_size = block_dataset_size
        self.augmentor = augmentor
        self.warehouses = warehouses
        self.__config_file = Path(__file__).parent / "configs" / "char_config.json"
        self.__font_whitelist = Path(__file__).parent / "configs" / "font_character_whitelist.json"
        self.font_folder = Path(__file__).parent / "data" / "fonts"
        self.__possible_fonts = {}
        self.__possible_lmdb = {}
        self._possible_scribe = []
        self.spacer = FixedSpacer(width=30)

        if "fonts" in warehouses:
            self.__possible_fonts = self._get_fonts()
            # print(self.__possible_fonts)
        if "block" in warehouses:
            self.__possible_lmdb = self._load_lmdb()
            # print(self.__possible_lmdb)
        if "cursive" in warehouses:
            # list of possible chars
            self._possible_scribe = self._load_scribe()

        with open(self.__config_file, "r") as f:
            self._chars_config = json.load(f)

        # list of possible characters for user to know what can be generated
        self.possible = set([*self.__possible_fonts] + list(self.__possible_lmdb.keys()) + self._possible_scribe)
        if self.possible == set():
            raise Exception("No data in the warehouses to choose from")

    def _load_lmdb(self):
        self._charset = Path.home() / ".inked" / self.block_dataset_size
        download_charset(self.block_dataset_size)
        self.lmdb = lmdb.open(str(self._charset))
        with open(self._charset / "details.json", "r") as f:
            return json.load(f)

    def _load_scribe(self):
        self.scribe = Scribe()
        return list(self.scribe.char_to_id.keys())

    def __getitem__(self, key: str) -> Character:
        """Generates a Character either from the font files or the MNIST style images supplied

        Args:
            key (Union[Tuple[str, int], str]): Either the character to generate as a string or a tuple with the character and exact image number

        Returns:
            Character: The requested character
        """
        assert isinstance(key, str)
        if key == r" ":
            return self.spacer(height=1)

        # randomly choose method of image except when explicitly given
        possible_warehouses = []
        if "fonts" in self.warehouses and self.__possible_fonts.get(key):
            possible_warehouses.append("fonts")
        if "block" in self.warehouses and self.__possible_lmdb.get(key):
            possible_warehouses.append("block")
        # This condition will not be reached until cursive is supported
        if "cursive" in self.warehouses and key in self._possible_scribe:  # pragma: no cover
            possible_warehouses.append("cursive")
        if len(possible_warehouses) == 0:
            raise KeyError

        generate_from = np.random.choice(possible_warehouses)

        if generate_from == "fonts":
            random_font = np.random.choice(self.__possible_fonts[key])
            img, font = self.generate_from_font(key, font=random_font)
            metadata = {"generator": "typefont", "font": font}
        elif generate_from == "block":
            rand_dataset = random_choice_arr(list(self.__possible_lmdb[key].keys()))
            rand_char_index = np.random.randint(1, self.__possible_lmdb[key][rand_dataset]["max"])
            img, font = self.generate_from_lmdb(key, rand_dataset, rand_char_index)
            metadata = {"generator": "inked", "font": font}
        # This condition will not be reached until cursive is supported
        elif generate_from == "cursive":  # pragma: no cover
            img, font = self.generate_from_scribe(key)
            metadata = {"generator": "scribe", "font": font}

        char = Character(key, image=img, metadata=metadata)
        if self.augmentor:
            char.augment(self.augmentor)

        return char

    def _get_fonts(self) -> Dict[str, List[str]]:
        """Pulls in all of the supplied fonts from the filesystem, filters out the
        characters using a whitelist and indexes them by the characters they support"""
        with open(self.__font_whitelist) as f:
            whitelist = json.load(f)

        fonts = {
            path.stem: {"glyphs": [chr(x) for x in TTFont(str(path))["cmap"].tables[-1].cmap.keys()], "path": path}
            for path in self.font_folder.glob("*.ttf")
        }

        supported: Dict[str, List[str]] = {}
        # {'a': ['Arial', ...], 'b': ['Helvetica', ...]}
        for fontname, font in fonts.items():
            for glyph in font["glyphs"]:  # type: ignore
                if glyph not in whitelist:
                    continue
                if supported.get(glyph) is None:
                    supported[glyph] = []
                supported[glyph].append(fontname)
        return supported

    def generate_from_font(
        self, glyph: str, font: Optional[Union[str, PurePath]] = None, size: int = 36
    ) -> Tuple[Image.Image, str]:
        """Generates a Image and font name for the requested glyph using font front the filesystem
        If the font is not supplied as a argument then a random font will be selected
        """
        padding = 2
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))

        font = self.font_folder / f"{np.random.choice(self.__possible_fonts[glyph])}.ttf"

        # NOTE: keeping fonts loaded into memory requires a size to be standardised
        ffont = ImageFont.truetype(str(font), size)
        drawing = ImageDraw.Draw(image)
        _, _, height, width = drawing.textbbox((0, 0), text=glyph, font=ffont, anchor="lt")

        drawing.text((0 + padding, 0 + padding), glyph, fill=(0, 0, 0, 255), font=ffont, anchor="lt", stroke_width=0)

        # glyph image out
        image = image.crop((0, 0, height + (padding * 2), width + (padding * 2)))

        # convert image from using transparency to show color to using rgb layers
        image = np.array(image)
        transparency = cv2.bitwise_not(image[:, :, 3])
        image[:, :, 0], image[:, :, 1], image[:, :, 2], image[:, :, 3] = (
            transparency,
            transparency,
            transparency,
            np.where(image[:, :, 3] == 0, 0, 255),
        )

        # attempting to remove white boarder around fonts
        image[:, :, 3] = np.where(image[:, :, 0] >= 200, 0, image[:, :, 3])
        image = darken_greys(image, 85)

        return image, font.stem

    def generate_from_lmdb(self, char: str, dataset: str, num: int) -> Tuple[Image.Image, str]:
        """Generates an image from the predownloaded LMDB file for the given character, dataset and number (composed into a key)"""
        key = f"{char}_{dataset}_{num:09d}"
        with self.lmdb.begin(write=False) as txn:
            imgbuf = txn.get(key.encode())
            buf = io.BytesIO()
            buf.write(imgbuf)
            buf.seek(0)
            img = Image.open(buf)
            img = white_to_transparent(img)
            # img = darken_greys(img, 127)
            return img, key

    def generate_from_scribe(self, key: str) -> Tuple[Image.Image, str]:
        """Generates a word using the scribe method (NN). Requires a key length of 3-4 characters"""
        return self.scribe.generate_sequence(text=key)


class WordGenerator(object):
    """Generates a word from with fixed or random spacing using the CharacterGenerator
    and applies any requested augmentations at both the word and character level"""

    def __init__(
        self,
        augmentor: Union[Augmentor, bool] = False,
        warehouses=["fonts", "block"],
        block_dataset_size: str = "sml",
    ):
        if isinstance(augmentor, Augmentor):
            self.augmentor = augmentor
        elif augmentor:
            self.augmentor = Augmentor()
        else:
            self.augmentor = None  # type: ignore

        self.chargen = CharacterGenerator(
            augmentor=self.augmentor, warehouses=warehouses, block_dataset_size=block_dataset_size
        )

    def generate(self, text: str, augment_word: bool = False, spacer: Union[FixedSpacer, RandomSpacer] = FixedSpacer()) -> Word:
        """Generates a Word from the requested text and spacing strategy, it will then apply any augmentations requested"""
        if "cursive" in self.chargen.warehouses:
            raise Exception(
                "Cursive is not currently supported with individual character generation. Please use the Word.generate_cursive function."
            )
        # Generate chars
        char_imgs = [self.chargen[char] for char in text]
        # Add in spaces
        word_list = []
        for i, char in enumerate(char_imgs):
            word_list.append(char)
            if i != len(char_imgs):
                space_char = spacer(char.image.height)
                word_list.append(space_char)

        # Create Word from the chars
        word = sum(word_list)
        if self.augmentor and augment_word:
            word = word.augment(self.augmentor)  # type: ignore
        return word  # type: ignore

    def generate_cursive(self, text: str, augment_word: bool) -> Word:
        """Generates a Word from the requested text using the scribe model, it will then apply any word augmentations requested"""
        assert all(
            [char in self.chargen._possible_scribe for char in text]
        ), "A character is not able to be made using the cursive scribe."

        image, font = self.chargen.generate_from_scribe(text)
        word = Word(text, image, metadata=[{"font": font}])

        if self.augmentor and augment_word:
            word = word.augment(self.augmentor)  # type: ignore
        return word
