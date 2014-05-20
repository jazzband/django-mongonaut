import os, sys
from setuptools import setup, find_packages

import mongonaut

LONG_DESCRIPTION = open('README.rst').read() + "\n\n"
CHANGELOG = open('CHANGELOG.rst').read()

LONG_DESCRIPTION += CHANGELOG

version = mongonaut.__version__

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='django-mongonaut',
    version=version,
    description="An introspective interface for Django and MongoDB",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='mongodb,django',
    author=mongonaut.__author__,
    author_email='pydanny@gmail.com',
    url='http://github.com/pydanny/django-mongonaut',
    license='MIT',
    packages=find_packages(exclude=['examples']),
    include_package_data=True,
    install_requires=['mongoengine>=0.5.2'],
    zip_safe=False,
    use_2to3 = True,
)
