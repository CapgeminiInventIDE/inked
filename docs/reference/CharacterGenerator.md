# Creating Characters

Generating a [Character](character.md) from a random method is easy. Simply initialise the `CharacterGenerator` class and choose a character to generate.

!!! Note:
    [WordGenerator](WordGenerator.md) can automatically setup a CharacterGenerator class (if required), removing the need for you to create individual characters yourself.

```python
from inked import CharacterGenerator

char_factory = CharacterGenerator()
char = char_factory["a"]

char.image.show()
char.save("output.png")
```

### CharacterGenerator Parameters

``` python
from inked import CharacterGenerator

char_factory = CharacterGenerator(warehouses = ['fonts', 'block'])
```

`warehouses:List[str] = ['fonts', 'block']` - Choose where character images are randomly generated from (default's both on).

- `['fonts']`: select character base image from a random Google font (alphanumeric, spaces and special characters).
- `['block']`: select character base image from a random handwritten image (alphanumeric and spaces only).

!!! Note:
    Currently only supports single character strings as input. For example, you are unable to specify a character using encoding such as ASCI.

``` python
from inked import CharacterGenerator, Augmentor

char_factory = CharacterGenerator(augmentor = Augmentor())
```

`augmentor: Optional[Augmentor] = None` - Determines if the character image will be augmented.

- `None`: (Default) No image augmentations will be used.
- `Augmentor`: Specify the augmentor and settings. See [Augmentor](Augmentor.md).

``` python
from inked import CharacterGenerator

char_factory = CharacterGenerator(warehouses = ['block'], block_dataset_size = 'sml')
```

`block_dataset_size:str = 'sml'` - determines which `block` warehouse to use (and downloads it if not already available).

- `sml`: (Default) Max 300 images for each alphanumeric character.
- `med`: Max 3000 images for each alphanumeric character.
- `lrg`: All images available for each alphanumeric character.
