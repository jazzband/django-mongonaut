#!/usr/bin/env python

import sys
import os

if sys.hexversion < 0x02070000:
     import unittest2 as unittest 
else: 
    import unittest 


#set path
TEST_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(TEST_ROOT, '..')
BLOG_ROOT = os.path.join(PROJECT_ROOT, 'examples','blog')

sys.path.append(PROJECT_ROOT)
sys.path.append(BLOG_ROOT) #we are using settings.py from the example

#Ensure Django is configured to use our example site
os.environ['DJANGO_SETTINGS_MODULE'] = 'examples.blog.settings'


#run the tests
tests = unittest.defaultTestLoader.discover(TEST_ROOT, pattern='*_tests.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(unittest.TestSuite(tests))
