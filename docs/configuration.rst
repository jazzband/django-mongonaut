=============
Configuration
=============

One of the most useful parts of `django.contrib.admin` is the ability to configure various views that touch and alter data. django-mongonaut is similar to the Django Admin, but adds in new functionality and ignores other features. The reason is that MongoDB is not a relational database, so attempting to replicate in general simply removes some of the more useful features we get from NoSQL.

Basic Pattern
==============

In your app, create a module called 'mongoadmin.py'. It has to be called that or django-mongonaut will not be able to find it. Then, in your new mongonaut file, simply import the mongoengine powered models you want mongonaut to touch, then import the MongoAdmin class, instantiate it, and finally attach it to your model.

.. sourcecode:: python

    # myapp/mongonaut.py

    # Import the MongoAdmin base class
    from mongonaut.sites import MongoAdmin

    # Import your custom models
    from blog.models import Post
    
    # Instantiate the MongoAdmin class        
    # Then attach the mongoadmin to your model
    Post.mongoadmin = MongoAdmin()
    
That's it! Now you can view, add, edit, and delete your MongoDB models!

.. note:: You will notice a difference between how and `django.contrib.admin` and `django-mongonaut` do configuration. The former associates the configuration class with the model object via a registration utility, and the latter does so by adding the configuration class as an attribute of the model object.