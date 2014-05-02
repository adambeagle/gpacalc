============
Installation
============

*Please note that this document assumes basic familiarity with 
Django, pip, and virtualenv.*

Dependencies
============

This project was developed for, and only tested with, Python 3.3. 
It has been designed to work with ``pip`` and ``virtualenv``. 
A requirements.txt file is included at the repository root that 
delineates the dependencies that can be installed via ``pip``.

Instructions
============

0. Optionally (but preferably), create a virtualenv with Python 3.3 as the default Python for use with the project.

1. From the root directory of the repository, ``pip install -r requirements.txt`` will install all necessary dependencies (Django, etc.).

2. The Django settings as given expect environment variables named  ``SECRET_KEY``, ``DB_USERNAME``, and ``DB_PASSWORD``. Either set these environment variables locally or hardcode values into the settings (located in ``gpacalc/gpacalc/settings/``). Consider using ``virtualenvwrapper``'s ``postactivate`` and ``predeactivate`` scripts to set/unset the environment variables automatically.

3. Configure the ``DATABASES`` setting in ``local.py`` in the settings directory. Note the project has only been tested with PostgreSQL.

4. ``syncdb``

5. The site should now be available to view at ``localhost:8000`` after ``runserver`` is run. 
