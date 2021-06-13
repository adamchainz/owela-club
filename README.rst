=============
Owela Central
=============

A Django project for playing the Namibian game of Owela against a dumb AI.
Built following the rules described on the `Mancala World wiki page for Owela <https://mancala.fandom.com/wiki/Owela>`__.

Running
-------

#. Make a Python 3.9 virtual environment with dependencies:

   .. code-block:: sh

       python3.9 -m venv venv
       source venv/bin/activate
       python -m pip install -U pip wheel
       python -m pip install -r requirements.txt

   The code was developed on Python 3.9 but may run on older versions.

#. Run the tests:

   .. code-block:: console

       pytest

   This should show output starting with:

   .. code-block:: text

       === test session starts ===

   …and finishing with output like:

   .. code-block:: text

       === 28 passed in 0.74s ===

#. Create the development database:

   .. code-block:: console

       python manage.py migrate

#. Start the development server.

   On Linux and macOS:

   .. code-block:: console

       DEBUG=1 python manage.py runserver

   On Windows:

   .. code-block:: console

       set DEBUG=1
       python manage.py runserver

Developing
----------

You’re free to edit the code already, but for the smoothest experience there are some extra tools you can set up.

First, there’s Editorconfig, which ensures your text editor is well configured for editing.
Install the appropriate `editorconfig plugin <https://editorconfig.org/>`__ for your text editor and the plugin will automatically confgiure your text editor based on the ``.editorconfig`` file.

Second, there’s pre-commit, which runs several code quality tools whenever you run ``git commit``.
These tools are configured in the ``.pre-commit-config.yaml`` file.
To set up pre-commit:

#. Install pre-commit by following its `instructions <https://pre-commit.com/#install>`__.
   You can use your virtual environment’s ``pip`` for the simplest setup.

#. Install the `pre-commit <https://pre-commit.com/>`__ hooks into your local repository:

   .. code-block:: sh

       pre-commit install

   This will configure Git to run pre-commit before each commit.

#. Check all files in the repository pass your pre-commit setup:

   .. code-block:: sh

       pre-commit run --all-files

   You should see many ``Passed`` messages, such as:

   .. code-block:: plain

       isort....................................................................Passed
       flake8...................................................................Passed

Extra tasks
-----------

This site has only been built as a demo of using htmx with Django.
It’s therefore missing some useful features for playing the game.
Here are some ideas of how to extend it...

* Deploy the game online by using hosting such as Heroku and following the `Django deployment checklist <https://docs.djangoproject.com/en/stable/howto/deployment/checklist/>`__.

* Make the board look good, maybe using a stony texture or showing the actual seeds.

* Display more information about the last two moves, such as highlighting selected squares and affected squares.

* Make the AI smarter - perhaps based on some heuristics such as “move from the biggest square” or “prefer moves on the inner row”.

* Have multiple AI functiosn and allow new games to pick which one to play against.

* Allow selecting different board widths.

* Allow rule variations such as `Hus <https://mancala.fandom.com/wiki/Hus>`__ or regional/house rules.

* Allow player-versus-player games.
  htmx’s `hx-trigger polling <https://dev.htmx.org/attributes/hx-trigger/>`__ can be used for simple updating of the board state.

* Add a login function so players can track their games.
