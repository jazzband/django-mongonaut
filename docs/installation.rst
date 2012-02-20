============
Installation
============

Normal Installation
===================

Get MongoDB::

    Download the right version per http://www.mongodb.org/downloads

Get the code::

    pip install django-mongonaut==0.2.11
    
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

Static Media Installation
=========================

By default, `django-mongonaut` uses static media hosted by other services such as Google or Github. 
If you need to point to another location, then you can change the following defaults to your new source:

.. sourcecode:: python

    # settings.py defaults
    MONGONAUT_JQUERY = "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
    MONGONAUT_TWITTER_BOOTSTRAP = "http://twitter.github.com/bootstrap/assets/css/bootstrap.css"
    MONGONAUT_TWITTER_BOOTSTRAP_ALERT = http://twitter.github.com/bootstrap/assets/js/bootstrap-alert.js"
    

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
