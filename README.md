# bplate
`bplate` is a command line tool for storing and generating boilerplates.

Using bplate, you can generate simple to complex boilerplates in matter of seconds.

## Installation
`bplate` can be installed using `pip`. **Python 3.8** or higher is required for
using this tool.
```sh
$ python -m pip install bplate
```

## Usage
`bplate` allows you to store a directory as boilerplate and use a simple command later
to generate code template from the stored boilerplate.

In order to store a directory as boilerplate, run `bplate new` command followed by
path of directory that you want to store as boilerplate (in this case, `web-app`).

When prompted, enter the name of boilerplate which will be used to reference it. The
boilerplate will be created.

```
$ bplate new ./web-app
...
Boilerplate name: simple-web-app
...
[!] Boilerplate created successfully!
```

A `bplate_config.json` will be created in the root directory. Whenever you want to
generate this boilerplate, simply run the `init` command followed by boilerplate name
and path where it should be generated:

```
$ bplate init simple-web-app ./my-project
```
