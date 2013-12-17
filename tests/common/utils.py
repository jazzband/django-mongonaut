#coding: utf-8
"""
 Copied exactly from https://github.com/hmarr/mongoengine/blob/master/mongoengine/django/tests.py

"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'examples.blog.settings'

import unittest
from django.test import TestCase, RequestFactory
from django.conf import settings

from mongoengine import connect

class MongoTestCase(TestCase):
    """
    TestCase class that clear the collection between the tests
    """
    db_name = 'test_%s' % settings.MONGO_DATABASE_NAME

    def __init__(self, methodName='runtest'):
        self.db = connect(self.db_name)
        super(MongoTestCase, self).__init__(methodName)

    def _post_teardown(self):
        super(MongoTestCase, self)._post_teardown()
        self.db.drop_database(self.db_name)

class DummyUser(object):

    def __init__(self, is_authenticated = True, is_active=True,
                    can_view=True, is_staff=True, is_superuser=False,
                 has_perm=['has_view_permission']):
        self._is_authenticated = is_authenticated
        self._is_active = is_active
        self._is_staff = is_staff
        self._is_superuser = is_superuser
        self._has_perm = has_perm

    def is_authenticated(self):
        return self._is_authenticated

    def has_perm(self, perm):
        return perm in self._has_perm

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_staff(self):
        return self._is_staff

    @property
    def is_superuser(self):
        return self._is_superuser
