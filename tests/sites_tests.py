#coding: utf-8
import unittest
from django.test import RequestFactory
from mongonaut.sites import BaseMongoAdmin  
from common.utils import DummyUser 

class BaseMongoAdminTests(unittest.TestCase):

    def setUp(self):
        self.req = RequestFactory().get('/')

    def testHasViewPermissions(self):
        self.req.user = DummyUser(is_authenticated=True, is_active=True)
        self.assertTrue(BaseMongoAdmin().has_view_permission(self.req))

    def testHasViewPermissionsInvalid(self):
        self.req.user = DummyUser(is_authenticated=False, is_active=True)
        self.assertFalse(BaseMongoAdmin().has_view_permission(self.req))

        self.req.user = DummyUser(is_authenticated=True, is_active=False)
        self.assertFalse(BaseMongoAdmin().has_view_permission(self.req))
        
        self.req.user = DummyUser(is_authenticated=False, is_active=False)
        self.assertFalse(BaseMongoAdmin().has_view_permission(self.req))

    def testHasEditPerms(self):
        self.req.user = DummyUser(is_authenticated=True, is_active=True,
                                  is_staff=True)

        self.assertTrue(BaseMongoAdmin().has_edit_permission(self.req))

    def testHasEditPermsInvalid(self):
        self.req.user = DummyUser(is_staff=False)
        self.assertFalse(BaseMongoAdmin().has_edit_permission(self.req))

        self.req.user = DummyUser(is_active=False)
        self.assertFalse(BaseMongoAdmin().has_edit_permission(self.req))
        
        self.req.user = DummyUser(is_authenticated=False)
        self.assertFalse(BaseMongoAdmin().has_edit_permission(self.req))

    
    def testHasAddPerms(self):
        self.req.user = DummyUser(is_authenticated=True, is_active=True,
                                  is_staff=True)
        
        self.assertTrue(BaseMongoAdmin().has_add_permission(self.req))

    def testHasAddPermsInvalid(self):
        self.req.user = DummyUser(is_staff=False)
        self.assertFalse(BaseMongoAdmin().has_add_permission(self.req))

        self.req.user = DummyUser(is_active=False)
        self.assertFalse(BaseMongoAdmin().has_add_permission(self.req))
        
        self.req.user = DummyUser(is_authenticated=False)
        self.assertFalse(BaseMongoAdmin().has_add_permission(self.req))


    def testHasDeletPerms(self):
        self.req.user = DummyUser(is_authenticated=True, is_active=True,
                                  is_superuser=True)
        
        self.assertTrue(BaseMongoAdmin().has_delete_permission(self.req))

    def testHasDeletePermsInvalid(self):
        self.req.user = DummyUser(is_superuser=False)
        self.assertFalse(BaseMongoAdmin().has_delete_permission(self.req))

        self.req.user = DummyUser(is_active=False, is_superuser=True)
        self.assertFalse(BaseMongoAdmin().has_delete_permission(self.req))
        
        self.req.user = DummyUser(is_authenticated=False, is_superuser=True)
        self.assertFalse(BaseMongoAdmin().has_delete_permission(self.req))


if __name__ == "__main__":
    unittest.main()

        
