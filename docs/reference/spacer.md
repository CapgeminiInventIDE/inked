# Spacer

Spacers are used by the [WordGenerator](WordGenerator.md) to place between each character when concatenating them together.

``` python
from inked.character import FixedSpacer, RandomSpacer
```

`FixedSpacer(width = 0)`: (Default) Sets the spacing to be 0px for each character concatenation.

`FixedSpacer(width = 10)`: Would add 10px to between each character concatenation.

`RandomSpacer(0, 10)`: Adds a random space with width 0px - 10px between each character.

!!! Note:
    Having a word string with a space in it (ie: *"Hello World"*) will add a `FixedSpacer(30)` as the space character (and still apply any additional spacing defined). This can be changed by assigning `CharacterGenerator.spacer = FixedSpacer(width=30)` after initialisation of either [WordGenerator](WordGenerator.md) or [CharacterGenerator](CharacterGenerator.md).
