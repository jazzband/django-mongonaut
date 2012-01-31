=====
API
=====

The following are advanced configuration features for django-mongonaut. Using them requires you to subclass the mongonaut.MongoAdmin class, then instantiate and attach your subclass as an attribute to the MongoEngine model.

.. note:: Future versions of mongonaut will allow you to work with pymongo collections without mongoengine serving as an intermediary.

Sample Usage
==============

.. sourcecode:: python

    # myapp/mongoadmin.py

    # Import the MongoAdmin base class
    from mongonaut.sites import MongoAdmin

    # Import your custom models
    from blog.models import Post
    
    # Subclass MongoAdmin and add a customization
    class PostAdmin(MongoAdmin):
    
        # Searches on the title field. Displayed in the DocumentListView.
        search_fields = ('title',)
        
        # provide following fields for view in the DocumentListView
        list_fields = ('title', "published", "pub_date")    
    
    # Instantiate the PostAdmin subclass        
    # Then attach PostAdmin to your model
    Post.mongoadmin = PostAdmin()

MongoAdmin Listing
===================

`mongonaut.sites.MongoAdmin.search_fields`
------------------------------------------

**default**: []

Accepts an iterable of string fields that matches fields in the associated model. Displays a search field in the DocumentListView. Performs an 'icontains' search with an 'OR' between evaluations. 

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):
    
        # Searches on the title field. Displayed in the DocumentListView.
        search_fields = ('title',)

`mongonaut.sites.MongoAdmin.list_fields`
----------------------------------------

**default**: Mongo _id

Accepts an iterable of string fields that matches fields in the associated model. Displays these fields as columns.

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):
    
    # provide following fields for view in the DocumentListView
    list_fields = ('title', "published", "pub_date")