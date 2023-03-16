.. _customization:

Customization
=============

When you create a boilerplate, a ``bplate_config.json`` is created in the root
directory which can be modified to change various aspect of the boilerplate. This
page shows the customization options that can be used in this file.

.. _customization-boilerplate-metadata:

Boilerplate Metadata
--------------------

The following keys are used to modify the metadata and information of boilerplate. This
metadata is generally used by the :ref:`bplate show <command-show>` command to show useful
information regarding a boilerplate. If you are distributing a boilerplate, these options
can be helpful.

.. _customization-name:

.. data:: name

    The name of boilerplate that it will be referenced with.

    This is one and the only required key in the ``bplate_config.json``. This key must
    be present in the config file in order for the boilerplate to work.

    While there are currently no limitations on setting names, it is recommended to use
    names that are easily referenced. Some guidelines for good naming are:

    - Use dashes (-) instead of spaces.
    - Use lowercase letters.
    - Don't start names with numbers

    :type:

        ``STRING``

.. _customization-description:

.. data:: description

    The description of boilerplate. There is currently no limitation on how long the
    description can be.

    :type:

        ``STRING``

.. _customization-version:

.. data:: version

    The version of boilerplate.

    :type:

        ``STRING``

.. _customization-author:

.. data:: author

    The name of boilerplate's author.

    :type:

        ``STRING``

.. _customization-url:

.. data:: url

    The URL pointing to boilerplate's homepage.

    :type:

        ``STRING``

Boilerplate Files
-----------------

.. _customization-ignore-patterns:

.. data:: ignore_patterns

    The list of glob-style patterns that should be ignored during creation
    of boilerplate.

    For example, in order to ignore files starting with ``test.``::

        {
            "ignore_patterns": [
                "test.*",
            ]
        }

    :type:

        ``ARRAY`` of ``STRING``
