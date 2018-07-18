.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

------------
Get Started!
------------

Ready to contribute? Here's how to set up ``magic-marker`` for local development using the handy built-in ``make`` tasks.
If you're not using virtualenvwrapper_ then just be aware that some of the available ``make`` tasks will not work.

Prerequisites
------------

In order to take full advantage of the built-in ``make`` tasks you must install virtualenvwrapper_ with the **system**
Python interpreter. Also, virtualenvwrapper_ must be fully configured and a virtual environment needs to be **active**
before running some of the ``make`` tasks specified in the next section.

Getting Help with Make Tasks
----------------------------

Execute the following command to get a full list of ``make`` tasks::

    $ make help

Using Make Tasks for Development Environment Setup
--------------------------------------------------

1. Fork the ``magic-marker`` repo on GitHub.
2. Create a virtual environment using virtualenvwrapper_ if you have not created one already::

    $ mkvirtualenv magic_marker

3. Clone your fork locally::

    $ git clone git@github.com:your_name_here/magic-marker.git

4. Setup develop environment::

    $ cd magic_marker/
    $ make develop-venv # OR 'make develop' if you're not using virtualenvwrapper

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ make test-all

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.
9. If you're running virtualenvwrapper_ then you can clean your virtual environment using this task::

    $ make clean-venv # OR 'make clean' if you're not using virtualenvwrapper

-----------------------
Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.4, 3.5 and 3.6, and for PyPy. Check
   https://travis-ci.org/rcbops/magic-marker/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

Get a list of available `make` tasks::

   $ make help

Install `magic-marker` into the active virtualenv::

   $ make install-venv # OR 'make install' if you're not using virtualenvwrapper

Run a subset of tests::

   $ py.test tests/test_magic_marker.py

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/