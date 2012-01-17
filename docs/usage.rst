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

Simple version. Create a mongonaut.py module in your app:

.. sourcecode:: python

    #myapp.mongonaut

    from mongonaut.sites import MongoAdmin

    from blog.models import Post
    
    Post.mongoadmin = MongoAdmin()


Complex version. Create a mongonaut.py module in your app:

.. warning:: This is is not fully implemented. Just use simple for now.

.. sourcecode:: python

    #myapp.mongonaut
    from datetime import datetime
    
    from mongonaut.sites import MongoAdmin
    
    from blog.models import Post
    
    class ArticleAdmin(MongoAdmin):
    
        search_fields = ['title',]
        
        #This shows up on the DocumentListView of the Posts
        list_actions = [publish_all_drafts,] 
        
        # This shows up in the DocumentDetailView of the Posts.
        document_actions = [generate_word_count,]
        
        field_actions = {confirm_images: 'image'}
        
        def publish_all_drafts(self):
            """ This shows up on the DocumentListView of the Posts """
            for post in Post.objects.filter(published=False):
                post.published = True
                post.pub_date = datetime.now()
                post.save()
                
        def generate_word_count(self):
            """ This shows up in the DocumentDetailView of the Posts. 
            ID in this case is somehow the ID of the Posting objecy
            """
            return len(Post.objects.get(self.id).content.split(' '))
            
        def confirm_images(self):
            """ This will be attached to a field in the generated form 
                specified in a dictionary
            """
            do_xyz()
            # TODO write this code or something like it
    
    Article.mongoadmin = ArticleAdmin()