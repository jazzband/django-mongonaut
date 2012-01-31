from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import StringField

class User(Document):
    email = StringField(required=True, max_length=50)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    
    def __unicode__(self):
        return self.email

class EmbeddedUser(EmbeddedDocument):
    email = StringField(required=True, max_length=50)
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
    pub_date = DateTimeField()
    published = BooleanField()
    creator = EmbeddedDocumentField(EmbeddedUser)    # for testing purposes

