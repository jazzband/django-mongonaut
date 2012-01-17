=============
Future Usage
=============

Complex version. Create a mongonaut.py module in your app:

.. warning:: This is is not fully implemented. Use it at your own extreme risk.

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