from mongoengine import Document, StringField, ReferenceField, ListField
from mongoengine import EmbeddedDocumentField, EmbeddedDocument

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))    

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()
    
    
class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)