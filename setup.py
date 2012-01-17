from setuptools import setup, find_packages
 
version = '0.2.1'

# TODO - add in dependencies
 
LONG_DESCRIPTION = """
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

    pip install django-mongonaut==0.2.1
    
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
"""
 
setup(
    name='django-mongonaut',
    version=version,
    description="An introspective interface for Django and MongoDB",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='mongo,django',
    author='Daniel Greenfeld',
    author_email='pydanny@gmail.com',
    url='http://github.com/pydanny/django-mongonaut',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)