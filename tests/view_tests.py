#coding: utf-8

import unittest
from django.test import RequestFactory
from mongonaut.views import IndexView 
from common.utils import DummyUser 

class IndexViewTests(unittest.TestCase):

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




if __name__ == "__main__":
    unittest.main()

        
