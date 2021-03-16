# Word Objects

The [WordGenerator](WordGenerator.md) methods `generate(text)` and `generate_cursive(text)` return a Word object.

```python
from inked import WordGenerator

factory = WordGenerator()
word = factory.generate("Hello World")
```

### Word Methods

```python
# save word image and all metadata
word.save('output.png')
```

- `word.save(path)`: Will save image to disc and attached all the augmentations and information (including the label or text of the image) as metadata within the saved image.
- `word.augment(augmentor=Augmentor())`: Manually apply augmentations to the word image. Works the same as specifying the Augmentor in `WordGenerator()` and setting `word_augment=True` with either `generate` or `generate_cursive` method.

!!! Note:
    Character and Word objects are almost identical in methods and attributes. The most notable difference is the augments available to each.

### Word Attributes

A given Word Instance will have the following attributes you can inspect and use.

With the above code, `word` will have a set of attributes you can inspect to understand what has been done to the image. These are similar to the `Character` class.

``` python
word.image.show()
# saves word image with no metadata
word.image.save("output.png")
```

- `word.image`: PIL.Image.Image of the word with any augmentations applied. This image will still have a transparent layer (although may be augmented to have a background color/image).

!!! Note:
    It is preferable to use word.save() method (see above) instead of using the Pillow package save. This will ensure the text/label, augmentations and their severity will be saved into the metadata of the file.

``` python
print(word.metadata)
```

- `word.metadata`: Stores a dict of what augmentations have been applied to the image at the **character level**, and at what severity level. Added to the metadata of the image when using the `word.save()` method.

``` python
print(word.word_metadata)
```

- `word.word_metadata`: Stores a dict of what augmentations have been applied to the image at the **word level**, and at what severity level. Added to the metadata of the image when using the `word.save()` method.

!!! Note:
    word.word_metadata will be an empty dict unless `augmentor = True` **and** `augment_word = True`.
