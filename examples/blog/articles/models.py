from mongoengine import Document, StringField, ReferenceField, ListField
from mongoengine import EmbeddedDocumentField, EmbeddedDocument

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    
class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)    

class Post(Document):
    # See Post.title.max_length to make validation better!
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    content = StringField()    
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))    

