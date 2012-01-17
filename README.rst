================
django-mongonaut
================
:Info: An introspective interface for Django and MongoDB.
:Author: Daniel Greenfeld (http://github.com/pydanny)

About
=====
Extracted from http://consumernotebook.com, django-mongonaut is an introspective interface for working with MongoDB via mongoengine. Rather then attempt to staple this functionality into Django's Admin interface, django-mongonaut takes the approach of rolling a new framework from scratch.

By writing it from scratch I get to avoid trying to staple ORM functionality on top of a NoSQL key/value store.

Support this project!
=====================

Sign up for an account on http://consumernotebook.com. It's free and always will be!

Installation
============

Get the code::

    pip install django-mongonaut==0.2.0
    
Install the dependency in your settings.py::

    INSTALLED_APPS = (
    ...
    'mongonaut',
    ...
    )
    
You will need the following also set up:

* django.contrib.sessions
* django.contrib.messages

    

Dependencies
============

- pymongo 1.1+
- mongoengine 0.5
- sphinx (optional - for documentation generation)

Features
=========

- Automatic introspection of mongoengine documents
- Ability to constrain who sees what and can do what.