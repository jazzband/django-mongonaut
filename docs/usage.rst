=====
Usage
=====

.. warning:: This is still in alpha. Use at your own discretion!

In your app's models.py create something:

.. sourcecode:: python

    # blog.models.py
    from mongoengine import BooleanField
    from mongoengine import Document
    from mongoengine import IntegerField    
    from mongoengine import StringField
    from mongoengine import FileField
    
    class Post(Document):
    
        title = StringField(max_length=255)
        slug = StringField(max_length=255)
        content = StringField()
        published = BooleanField(default=False)
        pub_date = DateTimeField()
        word_count = IntegerField()
        image = FileField()
        thumbnail = FileField()

MongoAdmin basics
==================

The easiest way to get your Model to be represented:

.. sourcecode:: python

    #myapp.mongonaut

    from mongonaut.sites import MongoAdmin

    from blog.models import Post
    
    Post.mongoadmin = MongoAdmin()

Complex MongoAdmin
==================

This gives you similar controls to what the Django ORM provides:

.. sourcecode:: python

    #myapp.mongonaut

    from mongonaut.sites import MongoAdmin

    from articles.models import Post, User

    class PostAdmin(MongoAdmin):

        def has_permission(self, request):
            # Overrides MongoAdmin default
            # Any user can view content
            #   even unauthenticated users        
            return True

        def has_staff_permission(self, request):
            # Overrides MongoAdmin default
            # Any user can view content
            #   even unauthenticated users
            return True

        # Provides a search field using Q objects
        #   so you can do ('title','content',) to check both
        search_fields = ('title',)


    Post.mongoadmin = PostAdmin()
    User.mongoadmin = MongoAdmin()




