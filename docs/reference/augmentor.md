# Augmentor

Used to morph Character and Word objects.

## Fully Custom Augmentor Setup

``` python
from inked import Augmentor

# specify your own config file
config = Path('path/to/json/config/file.json')
aug = Augmentor(config = config)
```

### Default config file and settings

Copy and save this as a file.json and pass it into the Augmentor() to customise how many augmentations, which augmentations and at what severity is applied (randomly selected between the min/max ranges).

``` json
[
    {
        "object": "Character",
        "min_augments": 1,
        "max_augments": 99,
        "augments": [
            { "name": "rotation", "enabled": true, "min_severity": -15, "max_severity": 15 },
            { "name": "scale_x", "enabled": true, "min_severity": 0.9, "max_severity": 1.1 },
            { "name": "scale_y", "enabled": true, "min_severity": 0.9, "max_severity": 1.1 },
            { "name": "text_fill", "enabled": true, "min_severity": [0,0,0], "max_severity": [255,255,255] },
            { "name": "text_texture", "enabled": true, "min_severity": 99, "max_severity": 99 }
        ]
    },
    {
        "object": "Word",
        "min_augments": 1,
        "max_augments": 99,
        "augments": [
            { "name": "rotation", "enabled": true, "min_severity": -3, "max_severity": 3 },
            { "name": "xblur", "enabled": true, "min_severity": 1, "max_severity": 2 },
            { "name": "yblur", "enabled": true, "min_severity": 1, "max_severity": 2 },
            { "name": "bg_image", "enabled": true, "min_severity": 99, "max_severity": 99 },
            { "name": "bg_colour", "enabled": true, "min_severity": 0.1, "max_severity": 0.4 },
            { "name": "random_pixel_noise", "enabled": true, "min_severity": 0.005, "max_severity": 0.03 }
        ]
    }
]
```

!!! Note:
    Where `min_severity` and `min_severity == 99`, those augmentations aren't affected by changes to severity. Severity was simply kept for consistancy in method variable handeling.

**Examples:**

- To keep the background transparent in the final word image, simply set `"enabled"` to `false` for both `bg_image` and `bg_colour` in the word augments.

- To disable character level augments, and reduce the maximum number of word augments, simply change the `min/max_augments` for each or set each Character augment to `false`.
