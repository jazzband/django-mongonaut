#coding: utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'examples.blog.settings'

import unittest
from django.test import RequestFactory
from mongonaut.views import IndexView 
from common.utils import DummyUser 

class ViewTests(unittest.TestCase):

    def setUp(self):
        self.req = RequestFactory().get('/')
        self.view = IndexView.as_view(template_name = "mongonaut/index.html")

    def testIndexViewReturnsValidPageWithProperPermissions(self):
        self.req.user = DummyUser()
    
        resp = self.view(self.req)
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.template_name[0], 'mongonaut/index.html')

    def testIndexViewRequiresViewPermissions(self):
        self.req.user = DummyUser(has_perm=['no_view_permissions'])
        
        
        resp = self.view(self.req)
        
        self.assertEquals(resp.status_code, 403)




'''class MongonautViewMixinTests(MongoTestCase, MongonautViewMixin, ListView):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.request = self.request_factory.request()

    def test_render_to_response_requires_permission(self):
        self.permission = 'has_view_permission'
        self.request.user = DummyUser(is_authenticated=False)
        self.assertEquals(1, self.render_to_response({}))
'''

if __name__ == "__main__":
    unittest.main()

        
