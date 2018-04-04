================
django-mongonaut
================
:Info: An introspective interface for Django and MongoDB.
:Version: 0.2.21
:Maintainer: Jazzband (jazzband.co)

.. image:: https://travis-ci.org/jazzband/django-mongonaut.png
   :alt: Build Status
   :target: https://travis-ci.org/jazzband/django-mongonaut

.. image:: https://codeclimate.com/github/jazzband/django-mongonaut/badges/gpa.svg
   :alt: Code Climate
   :target: https://codeclimate.com/github/jazzband/django-mongonaut

.. image:: https://jazzband.co/static/img/badge.svg
  :target: https://jazzband.co/
  :alt: Jazzband

This Project is Being Moved to Jazzband
=======================================

In late 2015 `@garrypolley`_ and I agreed to move this project to the `@jazzband`_ organization. Since we've both been off MongoDB for several years, maintaining this project ourselves no longer makes sense. By handing this to Jazzband, we are:

.. _`@garrypolley`: https://github.com/garrypolley
.. _`@jazzband`: https://github.com/jazzband

1. Putting the project in a place where it will be maintained and extended.
2. Removes the time and effort needed to continue to accept and manage pull requests for a project we no longer wish to maintain but has a somewhat active user base.

About
=====

django-mongonaut is an introspective interface for working with MongoDB via mongoengine. Rather then attempt to staple this functionality into Django's Admin interface, django-mongonaut takes the approach of rolling a new framework from scratch.

By writing it from scratch I get to avoid trying to staple ORM functionality on top of MongoDB, a NoSQL key/value binary-tree store.

Features
=========

- Automatic introspection of mongoengine documents.
- Ability to constrain who sees what and can do what.
- Full control to add, edit, and delete documents
- More awesome stuff! See https://django-mongonaut.readthedocs.io/en/latest/index.html#features

Installation
============

Made as easy as possible, setup is actually easier than `django.contrib.admin`. Furthermore, the only dependencies are mongoengine and pymongo. Eventually django-mongonaut will be able to support installations without mongoengine.

Get MongoDB::

    Download the right version per http://www.mongodb.org/downloads

Get Django Mongonaut (and mongoengine + pymongo)::

    pip install -U django-mongonaut

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

    from djanog import urls

    urlpatterns = [
        ...
        url.path('mongonaut/', urls.include('mongonaut.urls')),
        ...
    ]


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

* https://django-mongonaut.readthedocs.io/en/latest/api.html

Documentation
==============

All the documentation for this project is hosted at https://django-mongonaut.readthedocs.io.

Dependencies
============

- mongoengine >=0.5.2
- pymongo (comes with mongoengine)
- sphinx (optional - for documentation generation)

Code of Conduct
===============

This project follows the `Jazzband.co Code of Conduct`_.

.. _`Jazzband.co Code of Conduct`: https://jazzband.co/about/conduct
