.. django-mongonaut documentation master file, created by
   sphinx-quickstart on Mon Jan  2 09:26:02 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-mongonaut
================

This is an introspective interface for Django and MongoDB. Built from scratch to replicate some of the Django admin functionality, but for MongoDB.

Contents:

.. toctree::
   :maxdepth: 2
   
   installation
   usage
   configuration
   future_usage 
   
Features
========

(**Implemented items are in bold**)

* Introspection of Mongo data

    * **Introspection via mongo engine**
    * Introspection via pymongo (so you don't need to define a schema ahead of time)
    * **Q based searches**
    * **django.contrib.admin style browsing**
    * **Automatic detection of field types**
    * **Automatic discovery of collections**    
    * Admin determination of which fields are displayed
    
* Data Management

    * **Editing on all fields** except ListFields, EmbeddedFields, and ReferenceFields
    * **Automatic detection of widget types**
    * Text field shorthand for letting user quickly determine type when using without mongoengine
    * **Document Adds**
    * Document Deletes
    * Admin authored Collection level document control functions
    
* Permissions

    * **User level controls**
    * **Staff level controls**
    * **Admin defined controls**
    * Group defined controls    


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

