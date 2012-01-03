=====
Usage
=====

.. warning:: This is theoritical and does not work! Don't use this yet!

In your app's models.py create something:

.. sourcecode:: python

    # myapp.models.py
    from mongoengine import Document
    from mongoengine import StringField
    
    class Article(Document):
    
        title = StringField(max_length=255)
        slug = StringField(max_length=255)
    
Now create a mongonaut.py module in your app:

.. sourcecode:: python

    #myapp.mongonaut
    from mongonaut.sites import NautSite
    
    from myapp.models import Article
    
    NautSite.register(Article)
    
.. note:: Because of seeming limitations with mongoengine, we may need to specify the actual model definitions here, or scrape in the code to determine length of fields and stuff.