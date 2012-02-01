============
Installation
============

Normal Installation
===================

Get MongoDB::

    Download the right version per http://www.mongodb.org/downloads

Get the code::

    pip install django-mongonaut==0.2.8
    
Install the dependency in your settings file (settings.py):

.. sourcecode:: python

    INSTALLED_APPS = (
    ...
    'mongonaut',
    ...
    )
    
Also in your settings file, you'll need something like:

.. sourcecode:: python



    # mongodb connection
    from mongoengine import connect
    connect('example_blog')

You will need the following also set up:

* django.contrib.sessions
* django.contrib.messages

.. note:: No need for `autodiscovery()` with django-mongonaut!

Heroku MongoDB connection via MongoLabs
=======================================

Your connection string will be provided by MongoLabs in the Heroku config. To make that work, just use the following code instead the `# mongodb connection` example:

.. sourcecode:: python

    # in your settings file (settings.py)
    import os
    import re
    from mongoengine import connect
    regex = re.compile(r'^mongodb\:\/\/(?P<username>[_\w]+):(?P<password>[\w]+)@(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[_\w]+)$')
    mongolab_url = os.environ['MONGOLAB_URI']
    match = regex.search(mongolab_url)
    data = match.groupdict()
    connect(data['database'], host=data['host'], port=int(data['port']), username=data['username'], password=data['password'])
