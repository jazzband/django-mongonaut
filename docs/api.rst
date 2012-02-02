=====
API
=====

The following are advanced configuration features for django-mongonaut. Using them requires you to subclass the mongonaut.MongoAdmin class, then instantiate and attach your subclass as an attribute to the MongoEngine model.

.. note:: Future versions of mongonaut will allow you to work with pymongo collections without mongoengine serving as an intermediary.

MongoAdmin Objects
===================

class MongoAdmin
------------------

The MongoAdmin class is the representation of a model in the mongonaut interface. These are stored in a file named mongoadmin.py in your application. Let’s take a look at a very simple example of the MongoAdmin:

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

MongoAdmin Options
------------------

The MongoAdmin is very flexible. It has many options for dealing with customizing the interface. All options are defined on the MongoAdmin subclass:

`has_add_permission`
~~~~~~~~~~~~~~~~~~~~

**default**:

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):

        def has_add_permission(self, request):
            """ Can add this object """
            return request.user.is_authenticated and request.user.is_active and request.user.is_staff)

`has_edit_permission`
~~~~~~~~~~~~~~~~~~~~~~

**default**:

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):

        def has_delete_permission(self, request):
            """ Can delete this object """
            return request.user.is_authenticated and request.user.is_active and request.user.is_admin()

`has_edit_permission`
~~~~~~~~~~~~~~~~~~~~~~

**default**:

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):

        def has_edit_permission(self, request):
            """ Can edit this object """
            return request.user.is_authenticated and request.user.is_active and request.user.is_staff)

`has_view_permission`
~~~~~~~~~~~~~~~~~~~~~~

**default**:

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):

        def has_view_permission(self, request):
            """ Can view this object """
            return request.user.is_authenticated and request.user.is_active

`list_fields`
~~~~~~~~~~~~~~~~~~~~~~

**default**: Mongo _id

Accepts an iterable of string fields that matches fields in the associated model. Displays these fields as columns.

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):

        # provide following fields for view in the DocumentListView
        list_fields = ('title', "published", "pub_date")

`search_fields`
~~~~~~~~~~~~~~~~~~~~~~

**default**: []

Accepts an iterable of string fields that matches fields in the associated model. Displays a search field in the DocumentListView. Performs an 'icontains' search with an 'OR' between evaluations. 

.. sourcecode:: python

    # myapp/mongoadmin.py
    class PostAdmin(MongoAdmin):
    
        # Searches on the title field. Displayed in the DocumentListView.
        search_fields = ('title',)
