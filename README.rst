============
magic-marker
============


.. image:: https://img.shields.io/travis/rcbops/magic-marker.svg
        :target: https://travis-ci.org/rcbops/magic-marker


The magic-marker tool will read off the flake8 config and fix any missing marks that it is able to fix.

Fixable Marks
-------------

1. Marks that are configured to have value_match=uuid.  Magic Marker will read the configuration and generate the correct mark with a valid UUID as the argument.
2. Marks that are configured to have name=test_case_with_steps.  Magic Marker will generate a mark named 'test_case_with_steps' with no arguments.

Quick Start Guide
-----------------

1. Install ``magic-marker`` from PyPI with pip::

    $ pip install magic-marker

2. For more information on using the magic-marker launch help by::

    $ magic-marker --help


Contributing
------------

See `CONTRIBUTING.rst`_ for more details on developing for the magic-marker project.

Release Process
---------------

See `release_process.rst`_ for information on the release process for 'magic-marker'

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _CONTRIBUTING.rst: CONTRIBUTING.rst
.. _release_process.rst: docs/release_process.rst
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage