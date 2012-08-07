# -*- coding: utf-8 -*-

"""
The main purpose of these models is to do manual testing of
the mongonaut front end.  Do not use this code as an actual blog
backend.
"""

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


class Comment(EmbeddedDocument):
    message = StringField(default="DEFAULT EMBEDDED COMMENT")
    author = ReferenceField(User)

    # ListField(EmbeddedDocumentField(ListField(Something)) is not currenlty supported.
    # UI, and lists with list inside them need to be fixed.  The extra numbers appened to
    # the end of the key and class need to happen correctly.
    # Files to fix: list_add.js, forms.py, and mixins.py need to be updated to work.
    # likes = ListField(ReferenceField(User))


class EmbeddedUser(EmbeddedDocument):
    email = StringField(max_length=50, default="default-test@test.com")
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    created_date = DateTimeField()  # Used for testing
    is_admin = BooleanField()  # Used for testing
    # embedded_user_bio = EmbeddedDocumentField(Comment)
    friends_list = ListField(ReferenceField(User))

    # Not supportted see above comment on Comment
    # user_comments = ListField(EmbeddedDocumentField(Comment))


class Post(Document):
    # See Post.title.max_length to make validation better!
    title = StringField(max_length=120, required=True, unique=True)
    content = StringField(default="I am default content")
    author = ReferenceField(User, required=True)
    created_date = DateTimeField()
    published = BooleanField()
    creator = EmbeddedDocumentField(EmbeddedUser)
    published_dates = ListField(DateTimeField())
    tags = ListField(StringField(max_length=30))
    past_authors = ListField(ReferenceField(User))
    comments = ListField(EmbeddedDocumentField(Comment))

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.utcnow()
            if not self.creator:
                self.creator = EmbeddedUser()
                self.creator.email = self.author.email
                self.creator.first_name = self.author.first_name
                self.creator.last_name = self.author.last_name
        if self.published:
            self.published_dates.append(datetime.utcnow())
        super(Post, self).save(*args, **kwargs)
