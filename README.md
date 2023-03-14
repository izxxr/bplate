# bplate

bplate is a command line tool that allows you to create and store boilerplates.

Using bplate, you can store a directory as boilerplate template and easily
generate a boilerplate later using a simple command within matter of seconds.

## Installation
**Python 3.8 or higher is required to use this tool.**

bplate can easily be installed using the `pip` package manager:
```
python -m pip install bplate
```

## Basic Usage
To start using bplate, you first need to store a directory as boilerplate template. In
order to do that, use the `bplate new` followed by path of directory:
```
bplate new .\web-app-template
```

When prompted for boilerplate name, enter a name which will be used to reference to
boilerplate later:
```
$ bplate new .\web-app-template
...
Boilerplate name: simple-web-app
...
```

Once the boilerplate has been created, you can use the `bplate init` command to easily
generate boilerplate in a directory. The first argument is name of boilerplate that we
set earlier and second argument is the path where boilerplate is being generated:
```
bplate init simple-web-app .\my-web-app-project
```

## Customization
One of the main focus of bplate is to provide maximum customization and while this project
is in its early stages and there are not many options yet, we are constantly working on
bringing more customization options to the CLI.

When you create a boilerplate using the `bplate new`, a `bplate_config.json` file is
created in the root directory that can be edited to modify various aspect of the
boilerplate.

For all customization options, see the [Customization](https://bplate.readthedocs.io/en/stable/customization.html) page on the documentation.

## Contributing
bplate is currently in its early stage and we are constantly working on improving this
tool. You can help us improve bplate and any contribution in this regard will be
appreciated.

For more information, see the [Contributing to bplate](https://bplate.readthedocs.io/en/stable/contributing.html) page on the documentation.
