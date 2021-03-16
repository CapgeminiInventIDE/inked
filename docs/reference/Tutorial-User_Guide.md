# Basic Data Generation

Run a basic "Hello World" string creation with character and word augmentations.

``` python
from inked import WordGenerator

factory = WordGenerator(
                augmentor=True,
                warehouses=["fonts", "block"],
                block_dataset_size="sml"
            )

word = factory.generate("Hello World", augment_word=True)
word.save("Hello_World.png")

```

## Generating Images from a list of strings

You can quickly generate a random image with full augments from a given string with the simple setup below, saving images to disc with the metadata containing the text label, augmentations and their severity.

``` python
import numpy as np
from tqdm import tqdm
from inked import WordGenerator, FixedSpacer

np.random.seed(42)

def generate_list_of_word_images(words_list:list):
    factory = WordGenerator(
                    augmentor=True,
                    warehouses=["fonts", "block"],
                    block_dataset_size="sml"
                )

    for word_string in tqdm(words_list):
        word = factory.generate(word_string, augment_word=True, spacer=FixedSpacer(0))
        word.save(f"{word_string}.png")


if __name__ == "__main__":
    generate_list_of_word_images(words_list = ['Hello', 'World', 'Hello World'])
```

## Advanced Data Generation

The below setup allows you to save images to straight to LMDB format - saving IO write time when generating and reading in millions of images and their labels.
We've also added in a word generator to automatically select words to generate, along with manually specifying an Augmentor (see [Augmentor](Augmentor.md) to learn more about customising augmentations).

``` python
import numpy as np

from pathlib import Path
from tqdm import tqdm

from inked import WordGenerator, CharDict, RandomSpacer, Augmentor
from inked.lmdb_ctx import LMDBMaker

np.random.seed(42)


def random_word_images_to_lmdb(n_words: int, lmdb_folder: str):
    augmentor = Augmentor()
    factory = WordGenerator(
                    augmentor=augmentor,
                    warehouses=["cursive", "fonts", "block"],
                    block_dataset_size="lrg"
                )
    char_dict = CharDict(
        distribution={"english_words": 0.3, "google_words": 0.6, "additional_words": 0.1,},
        possible_chars=factory.chargen.possible,
    )

    # Generate a random word and save them to LMDB
    with LMDBMaker(Path(lmdb_folder)) as lmdb:
        for _ in tqdm(range(n_words)):
            rand_word = char_dict[char_dict.random_char]
            word = factory.generate(
                                rand_word,
                                augment_word = True,
                                spacer = RandomSpacer(_min = 0, _max = 20)
                            )
            lmdb.append(word.text, word.image.encode())



if __name__ == "__main__":
    random_word_images_to_lmdb(n_words = 1000, lmdb_folder = "LMDB")
```
