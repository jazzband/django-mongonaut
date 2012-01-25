from setuptools import setup, find_packages
 
version = '0.2.7'

# TODO - add in dependencies
 
LONG_DESCRIPTION = open('README.rst').read()
 
setup(
    name='django-mongonaut',
    version=version,
    description="An introspective interface for Django and MongoDB",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='mongodb,django',
    author='Daniel Greenfeld',
    author_email='pydanny@gmail.com',
    url='http://github.com/pydanny/django-mongonaut',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)