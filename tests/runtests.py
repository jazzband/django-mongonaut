#!/usr/bin/env python

#set path
import sys
sys.path.append("..")
sys.path.append("../examples/blog") #we are using settings.py from the example

#Ensure Django is configured to use our example site
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'examples.blog.settings'


#run the tests
import glob
import unittest

tests = unittest.defaultTestLoader.discover('.',pattern='*_tests.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(unittest.TestSuite(tests))
