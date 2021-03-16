import time
import typer
import numpy as np
import concurrent.futures

from pathlib import Path
from PIL import Image
from tqdm import tqdm

from src.inked import WordGenerator, CharDict, RandomSpacer, FixedSpacer, Augmentor
from src.inked.lmdb_ctx import LMDBMaker

# np.random.seed(42)


def main(n_words: int = 1):
    augmentor = Augmentor()
    factory = WordGenerator(
        augmentor=augmentor, warehouses=["fonts", "block"], block_dataset_size="sml"
    )  # 'cursive'
    char_dict = CharDict(
        distribution={"english_words": 0.1, "google_words": 0.6, "additional_words": 0.3,},
        possible_chars=factory.chargen.possible,
    )

    # LMDB
    # with LMDBMaker(Path("LMDB")) as lmdb:
    #     for _ in tqdm(range(n_words)):
    #         rand_word = char_dict[char_dict.random_char]
    #         word = factory.generate(rand_word, augment_word=True, spacer=RandomSpacer(0))
            # lmdb.append(word.text, word.image)

    # NORMAL
    st = time.time()
    for i in tqdm(range(n_words)):
        char = char_dict.random_char
        rand_word = char_dict[char]
        # word = factory.generate("SpaceX", augment_word=True, spacer=FixedSpacer(0))
        word = factory.generate_cursive("hello", augment_word=True)
        word.save("demo.png")

    print(time.time() - st)


if __name__ == "__main__":
    typer.run(main)
