.. django-mongonaut documentation master file, created by
   sphinx-quickstart on Mon Jan  2 09:26:02 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-mongonaut
================

This is an introspective interface for Django and MongoDB. Built from scratch to replicate some of the Django admin functionality, but for MongoDB.

Contents:

.. toctree::
   :maxdepth: 3
   
   installation
   configuration
   api
   future_usage 
  


   
Features
========

Introspection of mongoengine data
----------------------------------

    * Introspection via mongo engine
    * Q based searches
    * django.contrib.admin style browsing
    * Automatic detection of field types
    * Automatic discovery of collections    

Introspection of pymongodata
-----------------------------

    * **[in progress]** Admin determination of which fields are displayed. Currently they can do so in the Document List view but not the Document Detail view.
    * **[in progress]** Introspection via pymongo. This is becoming very necessary. Plan:

        * Always guarantee the _id.
        * Allow devs to set 1 or more field as 'expected'. But there is no hard contract!
        * introspect on field types to match how pymongo pulls data. So a `str` is handled differently than a list field.
    
Data Management
----------------------------

    * **[in progress]** Editing on ListFields and EmbeddedDocumentsFields
    * **[in progress]** Admin authored Collection level document control functions
    * Document Deletes    
    * Editing on most other fields including ReferenceFields.
    * Automatic detection of widget types
    * Text field shorthand for letting user quickly determine type when using without mongoengine
    * Document Adds
    
Permissions
----------------------------

    * **[in progress]** Group defined controls    
    * User level controls
    * Staff level controls
    * Admin defined controls


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

