================
django-mongonaut
================
:Info: An introspective interface for Django and MongoDB.
:Author: Daniel Greenfeld (http://github.com/pydanny)

About
=====
Extracted from http://consumernotebook.com, django-mongonaut is an introspective interface for working with MongoDB via mongoengine. Rather then attempt to staple this functionality into Django's Admin interface, django-mongonaut takes the approach of rolling a new framework from scratch.

By writing it from scratch I get to avoid trying to staple ORM functionality on top of a NoSQL key/value store.

Features
=========

- Automatic introspection of mongoengine documents.
- Ability to constrain who sees what and can do what.
- Full control to add, edit, and delete documents
- More more! See http://django-mongonaut.readthedocs.org/en/latest/index.html#features

Installation
============

See: http://django-mongonaut.readthedocs.org/en/latest/installation.html


Configuration
=============

See: http://django-mongonaut.readthedocs.org/en/latest/configuration.html

Documentation
==============

You can find out how to install and use this project at http://django-mongonaut.rtfd.org.

Support this project!
=====================

Sign up for an account on http://consumernotebook.com. It's free and always will be!




    

Dependencies
============

- pymongo 1.1+
- mongoengine 0.5
- sphinx (optional - for documentation generation)

