# Character Objects

Create a Character object by using the CharacterGenerator method `__getitem__`.

!!! Note:
    While you are able to create individual characters (outlined below) this is not required to generate word images at it will all be taken care of for you in the WordGenerator class. See [WordGenerator](WordGenerator.md) for more information and examples.

```python
from inked import CharacterGenerator

chargen = CharacterGenerator()
char = chargen["a"]
char2 = chargen["b"]
```

## Character Methods

```python
# save char image and all metadata
char.save('output.png')

# adds chars together to create a word object.
word = sum([char, char2])
```

- `sum([char, char2])`: Adds (concatinates left to right) two or more Character instances together, returning a `Word` instance (see [Word](word.md)).
- `char.save(path)`: Will save image to disc and attached all the augmentations and information (including the label or text of the image) as metadata within the saved image.
- `char.augment(augmentor=Augmentor())`: Manually apply augmentations to the character image. Works the same as specifying the Augmentor in CharacterGenerator().

## Character Attributes

```python
# use PIL to show the image
char.image.show()

# print what augmentations have been applied to the character image
print(char.metadata)
```

With the above code, `char` will have a set of attributes you can inspect to understand what has been done to the image.

- `char.image`: PIL.Image.Image of the character plus any augmentations. This image will still have a transparent background.
- `char.metadata`: Stores a dict of what augmentations have been done to the image at what severity levels.

!!! Note:
    Character and [Word](word.md) objects are almost identical in methods and attributes. The most notable difference is the augments available to each.