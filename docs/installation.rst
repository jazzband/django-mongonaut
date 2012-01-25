============
Installation
============

Get MongoDB::

    Download the right version per http://www.mongodb.org/downloads

Get the code::

    pip install django-mongonaut==0.2.7
    
Install the dependency in your settings.py::

    INSTALLED_APPS = (
    ...
    'mongonaut',
    ...
    )
    
You will need the following also set up:

* django.contrib.sessions
* django.contrib.messages

.. note:: No need for `autodiscovery()` with django-mongonaut!