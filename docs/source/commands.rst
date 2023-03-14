.. _commands:

Commands
========

This page documents all the available commands in bplate.

.. _commands-bplate-information:

bplate Information
------------------

.. _command-version:

.. data:: bplate version [--all]

    Shows bplate version.

    :flags:

        ``--all``: When set, shows other information about bplate and user's machine.

.. _commands-boilerplates-management:

Boilerplates Management
-----------------------

These commands are used to manage stored boilerplates.

.. _command-new:

.. data:: bplate new PATH

    Creates and stores a new boilerplate from the given path.

    If a ``bplate_config.json`` exists in the given directory, the name of
    boilerplate will be loaded from that file otherwise user will be prompted
    to enter the boilerplate name.

    :arguments:
        
        ``PATH``: The path pointing to directory that should be stored as boilerplate.
        This argument must be point to an existing and readable directory.

.. _command-delete:

.. data:: bplate delete NAME

    Deletes a stored boilerplate.

    :arguments:

        ``NAME``: The name of boilerplate to delete.

.. _command-list:

.. data:: bplate list

    Lists the names of all the stored boilerplates.

.. _command-show:

.. data:: bplate show NAME

    Shows details about a stored boilerplate.

    :arguments:

        ``NAME``: The name of boilerplate to show information of.

.. _commands-boilerplate-generation:

Boilerplate Generation
----------------------

These commands aid in generation of boilerplates.

.. _command-init:

.. data:: bplate init NAME PATH

    Initializes a boilerplate at the given path.

    :arguments:

        ``NAME``: The name of stored boilerplate to generate from.

        ``PATH``: The directory where the boilerplate should be generated. If the
        given path does not point to an existing directory, it will be created.
