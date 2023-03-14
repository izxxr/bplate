.. bplate documentation master file, created by
   sphinx-quickstart on Tue Mar 14 09:40:48 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bplate's documentation!
==================================

bplate is a command line tool that allows you to create and store boilerplates.

Using bplate, you can store a directory as boilerplate template and easily
generate a boilerplate later using a simple command within matter of seconds.

Installation
------------

**Python 3.8 or higher is required to use this tool.**

bplate can easily be installed using the ``pip`` package manager::

   python -m pip install bplate

Basic Usage
-----------

To start using bplate, you first need to store a directory as boilerplate template. In
order to do that, use the :ref:`bplate new <command-new>` followed by path of directory::

   bplate new .\web-app-template

When prompted for boilerplate name, enter a name which will be used to reference to
boilerplate later::

   $ bplate new .\web-app-template
   ...
   Boilerplate name: simple-web-app
   ...

Once the boilerplate has been created, you can use the :ref:`bplate init <command-init>`
command to easily generate boilerplate in a directory. The first argument is name of
boilerplate that we set earlier and second argument is the path where boilerplate is being
generated::

   bplate init simple-web-app .\my-web-app-project

Customization
-------------

One of the main focus of bplate is to provide maximum customization and while this project
is in its early stages and there are not many options yet, we are constantly working on
bringing more customization options to the CLI.

When you create a boilerplate using the :ref:`bplate new <command-new>`, a ``bplate_config.json``
file is created in the root directory that can be edited to modify various aspect of the boilerplate.

For all customization options, see the ":ref:`customization`" section.

Contributing
------------

bplate is currently in its early stage and we are constantly working on improving this
tool. You can help us improve bplate and any contribution in this regard will be
appreciated.

For more information, see the ":ref:`contributing`" section.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   commands
   customization
   contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
