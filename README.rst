=============
Owela Central
=============

A Django project for playing the Namibian game of Owela against a dumb AI, following the rules described on the `Mancala World wiki <https://mancala.fandom.com/wiki/Owela>`__.

Setting up
----------

#. Install pre-commit by following its `instructions <https://pre-commit.com/#install>`__.

#. Make a Python 3.9 virtual environment with dependencies:

   .. code-block:: sh

       python3.9 -m venv venv
       source venv/bin/activate
       python -m pip install -U pip wheel
       python -m pip install -r requirements.txt


#. Run the tests:

   .. code-block:: sh

       pytest

   This checks everything is good to go.
   Django creates a temporary database during the test run.

#. Install the `pre-commit <https://pre-commit.com/>`__ hooks:

   .. code-block:: sh

       pre-commit install

   This runs code quality and formatting checks every time you commit, such as Black and Flake8.

#. Check all files in the repository pass your pre-commit setup:

   .. code-block:: sh

       pre-commit run --all-files

#. Install the `editorconfig plugin <https://editorconfig.org/>`__ for your text editor.

#. Set up the development database:

   .. code-block:: console

       python manage.py migrate

   This creates the development database.

#. Start the development server:

   .. code-block:: console

       DEBUG=1 python manage.py runserver

Extensions
----------

This site has been built as a demo of Django with htmx.
It’s therefore missing some useful features.
Here are some ideas of how to extend it...

* Deploy the game online by using hosting such as Heroku and following the `Django deployment checklist <https://docs.djangoproject.com/en/stable/howto/deployment/checklist/>`__.

* Make the board look nicer.

* Display more information about the last two moves, such as highlighting selected squares and affected squares.

* Make the AI smarter - perhaps based on some heuristics such as “move the biggest square” or “prefer to move on the inner row”.
  Allow selection of which AI to play against.

* Allow selecting different board widths.

* Allow the rule variations such as `Hus <https://mancala.fandom.com/wiki/Hus>`__, and other regional house rules.

* Allow player-versus-player games.
  htmx’s `hx-trigger polling <https://dev.htmx.org/attributes/hx-trigger/>`__ can be used for simple updating of the board state.

* Add login so players can track their games.
