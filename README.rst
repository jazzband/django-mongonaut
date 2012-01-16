================
django-mongonaut
================
:Info: An introspective interface for Django and Mongo.
:Author: Daniel Greenfeld (http://github.com/pydanny)

About
=====
Extracted from http://consumernotebook.com, django-mongonaut is an introspective interface for working with Mongo via mongoengine. Rather then attempt to staple this functionality into Django's Admin interface, django-mongonaut takes the approach of rolling a new framework from scratch.

By writing it from scratch I get to avoid trying to staple ORM functionality on top of a NoSQL key/value store.

Support this project!
=====================

Sign up for an account on http://consumernotebook.com. It's free and always will be!

Installation
============

Not yet! This is pre-alpha, and I'm still abstracting/enhancing/extracting from production code.

Dependencies
============

- pymongo 1.1+
- mongoengine 0.5
- sphinx (optional - for documentation generation)

Features
=========

- Automatic introspection of mongoengine documents
- Ability to constrain who sees what and can do what.