# Creating Words with WordGenerator

Generating a [Word](word.md) image from a string is easy. Simply initialise the `WordGenerator` class and choose a string to generate.

``` python
from src.inked import WordGenerator

factory = WordGenerator()
word = factory.generate("Hello World")

# display or save out the image
word.image.show()
word.save("output.png")
```

Under the hood, this is actually initializing a [CharacterGenerator](CharacterGenerator.md) and generating individual [character](character.md)s, adding them together to create the final [Word](word.md) object.

### WordGenerator Parameters

``` python
from src.inked import WordGenerator

factory = WordGenerator(warehouses = ['fonts', 'block'])
```

`warehouses:List[str] = ['fonts', 'block', 'cursive']` - Choose where character images are randomly generated from (default's all).

- `['fonts']`: select individual character images from a random Google font (alphanumeric, spaces and special characters) which is then added/concatinated together with others to form the word.
- `['block']`: select individual character images from a handwritten image (alphanumeric and spaces only) which is then added/concatinated together with others to form the word.
- `['cursive']`: constructs the entire word as a single string using a Neural  Network (currently alphanumeric only).
!!! Note:
    `cursive` requires a word length of 3+ characters and does not support character level augmentations as the entire string is generated at once.


``` python
from src.inked import WordGenerator

factory = WordGenerator(augmentor = True)
```

`augmentor:Union[Bool, Augmentor()] = False` - Sets the augmentor and determines if character level augmentations will be performed.

- `False`: (Default) No image augmentations will be used.
- `True`: Enables the default Augmentor and applies a random selection of augments on each character image (separately).
- `Augmentor`: Specify your own augmentor and settings. See [Augmentor](Augmentor.md).

### WordGenerator Methods

```python
from src.inked import WordGenerator

factory = WordGenerator()

# generate words using block and fonts warehouses
word = factory.generate("Hello World")
```

`generate(text)`: generates the given text as individual characters, before added them together to complete the word image.

#### **Parameters**

- `text: str`: (Required) the text string to generate.
- `augment_word: bool`: Enables word level augmentations (Augmentor is required to be set).
- `spacer: Union[FixedSpacer, RandomSpacer]`: The amount of space applied to each character when forming a word (defaults to `FixedSpacer(0)`) See [spacer](spacer.md).

``` python
# generate words using the cursive neural network
cursive_word = factory.generate_cursive("Hello World")
```

`generate_cursive(text)`: generates a full word image from a neural network (requires length of text to be > 3)

#### **Parameters**

- `text: str`: (Required) the text string to generate.
- `augment_word: bool`: Enables word level augmentations (Augmentor is required to be set).

!!! Note:
    `generate_cursive` is not able to be used with character level augmentations.