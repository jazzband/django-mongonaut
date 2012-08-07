# -*- coding: utf-8 -*-

from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import StringField

from datetime import datetime


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
    created_date = DateTimeField()
    published = BooleanField()
    creator = EmbeddedDocumentField(EmbeddedUser)    # for testing purposes
    wanted_published = ListField(BooleanField())  # used for testing boolean list
    published_dates = ListField(DateTimeField())  # used for testing datefield lists
    past_authors = ListField(ReferenceField(User))  # used for testing reference fields

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.utcnow()
        if self.published:
            self.published_dates.append(datetime.utcnow())
        super(Post, self).save(*args, **kwargs)
