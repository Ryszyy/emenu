eMenu
=====

eMenu - Menu cards API

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT



Build the Stack
---------------

This can take a while, especially the first time:
::

$ docker-compose -f local.yml build

Run the Stack
-------------

This brings up both Django and PostgreSQL.
The first time it is run it might take a while to get started,
but subsequent runs will occur quickly.
::

$ docker-compose -f local.yml up

Execute Management Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

$ docker-compose -f local.yml run --rm django python manage.py migrate
$ docker-compose -f local.yml run --rm django python manage.py createsuperuser

Type checks and linting
^^^^^^^^^^^^^^^^^^^^^^^

Running type checks with mypy:

::

 $ docker-compose -f local.yml run --rm django flake8
 $ docker-compose -f local.yml run --rm django mypy emenu


Testing
^^^^^^^
Run test and report coverage
::

 $ docker-compose -f local.yml run --rm django pytest
 $ docker-compose -f local.yml run --rm django coverage run -m pytest
 $ docker-compose -f local.yml run --rm django coverage report
