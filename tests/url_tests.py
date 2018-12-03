#coding: utf-8

import unittest
from importlib import import_module

from django.test import RequestFactory
from bson.objectid import ObjectId
from django.core.urlresolvers import NoReverseMatch
from django.conf import settings
import django

from mongonaut.views import DocumentDetailView
from common.utils import DummyUser
from examples.blog.articles.models import Post, NewUser
from mongonaut.templatetags.mongonaut_tags import get_document_value


class IndexViewTests(unittest.TestCase):

    def setUp(self):
        self.req = RequestFactory().get('/')
        django.setup()

    def testURLResolver(self):
        '''
            Tests whether reverse function inside get_document_value can 
            correctly return a document_detail url when given a set of:
            <document_name> <app_label> and <id>
            Both <document_name> and <app_label> will contain dots, eg.
                <document_name> : 'User.NewUser'
                <app_label>     : 'examples.blog.articles'
        '''

        urls_tmp = settings.ROOT_URLCONF
        settings.ROOT_URLCONF = 'examples.blog.urls'

        u = NewUser(email='test@test.com')
        u.id=ObjectId('abcabcabcabc')

        p = Post(author=u, title='Test')
        p.id = ObjectId('abcabcabcabc')

        match_found = True

        try:
            v = get_document_value(p, 'author')
        except NoReverseMatch as e:
            match_found = False

        settings.ROOT_URLCONF = urls_tmp

        self.assertEquals(match_found, True)

    def testDetailViewRendering(self):
        '''
            Tries to render a detail view byt giving it data 
            from examples.blog. As <app_label> and <document_name>
            may contain dots, it checks whether NoReverseMatch exception
            was raised.
        '''

        self.req.user = DummyUser()

        urls_tmp = settings.ROOT_URLCONF
        settings.ROOT_URLCONF = 'examples.blog.urls'

        self.view = DocumentDetailView.as_view()(
                        app_label='examples.blog.articles', 
                        document_name='Post', 
                        id=ObjectId('abcabcabcabc'),
                        request=self.req, 
                        models=import_module('examples.blog.articles.models')
                    )

        match_found = True

        try:
            self.view.render()
        except NoReverseMatch as e:
            match_found = False

        settings.ROOT_URLCONF = urls_tmp
        
        self.assertEquals(match_found, True)

    def testUnicodeURLResolver(self):
        '''
            Similarly to testURLResolver, it tests whether get_document_value does not throw an exception.
            This time, the value with unicode characters is provided.
        '''
        
        settings.ROOT_URLCONF = 'examples.blog.urls'

        # Some unicode characters

        email = u"ąćźżńłóśę@gmail.com"

        u = NewUser(email=email)
        u.id=ObjectId('abcabcabcabc')

        p = Post(author=u, title='Test Post')
        p.id = ObjectId('abcabcabcabc')

        unicode_ok = False

        try:
            res = get_document_value(p, 'author')
            unicode_ok = True
        except UnicodeEncodeError as e:
            pass

        self.assertTrue(unicode_ok)

if __name__ == "__main__":
    unittest.main()
