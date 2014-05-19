================
django-mongonaut
================
:Info: An introspective interface for Django and MongoDB.
:Version: 0.2.21
:Maintainer: Daniel Greenfeld (http://pydanny.com)

.. image:: https://travis-ci.org/pydanny/django-mongonaut.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/django-mongonaut

About
=====

django-mongonaut is an introspective interface for working with MongoDB via mongoengine. Rather then attempt to staple this functionality into Django's Admin interface, django-mongonaut takes the approach of rolling a new framework from scratch.

By writing it from scratch I get to avoid trying to staple ORM functionality on top of MongoDB, a NoSQL key/value binary-tree store.

Features
=========

- Automatic introspection of mongoengine documents.
- Ability to constrain who sees what and can do what.
- Full control to add, edit, and delete documents
- More awesome stuff! See http://django-mongonaut.readthedocs.org/en/latest/index.html#features

Installation
============

Made as easy as possible, setup is actually easier than `django.contrib.admin`. Furthermore, the only dependencies are mongoengine and pymongo. Eventually django-mongonaut will be able to support installations without mongoengine.

Get MongoDB::

    Download the right version per http://www.mongodb.org/downloads
    
Get mongoengine (and pymongo):

    pip install mongoengine=>0.5.2

Get the code::

    pip install django-mongonaut==0.2.20
    
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

Add the mongonaut urls.py file to your urlconf file:

.. sourcecode:: python

    urlpatterns = patterns('',
        ...
        (r'^mongonaut/', include('mongonaut.urls')),
        ...
    )


Configuration
=============

django-mongonaut will let you duplicate much of what `django.contrib.admin` gives you, but in a way more suited for MongoDB. Still being implemented, but already works better than any other MongoDB solution for Django. A simple example::

    # myapp/mongoadmin.py

    # Import the MongoAdmin base class
    from mongonaut.sites import MongoAdmin

    # Import your custom models
    from blog.models import Post

    # Instantiate the MongoAdmin class        
    # Then attach the mongoadmin to your model
    Post.mongoadmin = MongoAdmin()

* http://django-mongonaut.readthedocs.org/en/latest/api.html

Documentation
==============

All the documentation for this project is hosted at http://django-mongonaut.rtfd.org.

Dependencies
============

- mongoengine >=0.5.2
- pymongo (comes with mongoengine)
- sphinx (optional - for documentation generation)

Support this project!
======================

You can hire the lead maintainer to perform dedicated work on this package. Please email pydanny@cartwheelweb.com.
