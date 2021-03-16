<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Invent_Logo_2COL_RGB.png" style="width:80%;"><br>
</div>

-----------

# inked

[![Documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://CapgeminiInventIDE.github.io/inked/)
[![Course Content Evolving](https://img.shields.io/badge/Course%20Content-Evolving-green.svg)](https://CapgeminiInventIDE.github.io/inked/)
[![Discord](https://img.shields.io/discord/752353026366242846.svg?label=Join%20us%20on%20Discord&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/rQcMtVE)
[![License](https://img.shields.io/pypi/l/doc_loader.svg)](https://github.com/CapgeminiInventIDE/inked/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Run on repl.it](https://docs.repl.it/images/repls/run-on-replit.svg)](https://repl.it/github/CapgeminiInventIDE/inked)

Evolving repo of the inked

## Usage


String-to-Image generation tool, designed to speed up data generation in Natural Language Processing, Scene Text Detection and other text as image projects.

Run a basic Hello World text as image generation.

``` python
from inked import WordGenerator

factory = WordGenerator()
word = factory.generate("Hello World")

word.save("Hello_World.png")
```

Generate images with no augmentations (transparent background removed for viewing):

![Hello World No Augmentations](docs/assets/imgs/hello_world_no_augments.png)

Or augment each individual character and the whole word to create truly endless images:

![Hello World Augmentations](docs/assets/imgs/hello_world_augments.png)

![Hello World Augmentations2](docs/assets/imgs/hello_world_augments2.png)

For more advanced setups see our [User Guide](https://github.com/CapgeminiInventIDE/inked/tree/main/docs/reference/Tutorial-User_Guide.md).
## License

* [Mozilla Public License 2.0](/LICENSE)

## Contributing

1. Fork the repository
2. Create a branch in your own fork: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request back to our fork.

## About Us

### Capgemini Invent combines strategy, technology, data science and creative design to solve the most complex business and technology challenges.

Disruption is not new, but the pace of change is. The fourth industrial revolution is forcing businesses to rethink everything they know.

Leading organizations behave as living entities, constantly adapting to change. With invention at their core, they continuously redesign their business to generate new sources of value. Winning is about fostering inventive thinking to create what comes next.

### Invent. Build. Transform.

This is why we have created Capgemini Invent, Capgemini’s new digital innovation, consulting and transformation global business line. Our multi-disciplinary team helps business leaders find new sources of value. We accelerate the process of turning ideas into prototypes and scalable real-world solutions; leveraging the full business and technology expertise of the Capgemini Group to implement at speed and scale.

The result is a coordinated approach to transformation, enabling businesses to create the products, services, customer experiences, and business models of the future.

## We're Hiring!

Do you want to be part of the team that builds doc_loader and [other great products](https://github.com/CapgeminiInventIDE) at Capgemini Invent? If so, you're in luck! Capgemini Invent is currently hiring Data Scientists who love using data to drive their decisions. Take a look at [our open positions](https://www.capgemini.com/careers/job-search/?search_term=capgemini+invent) and see if you're a fit.
