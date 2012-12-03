# -*- coding: utf-8 -*-
from distutils.core import setup
import djangocms_gallery

import os


VERSION = djangocms_gallery.__version__
AUTHOR = djangocms_gallery.__author__
NAME = 'djangocms-gallery'
URL = 'https://github.com/pascalmouret/djangocms-gallery'
AUTHOR_MAIL = 'pascal.mouret@divio.ch'
DESCRIPTION = 'Gallery plugin for the django-cms.'
README = 'README.md'

REQUIREMENTS = [
    'django-filer',
    'easy-thumbnails',
]

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

# make it work
if not 'a' in VERSION and not 'b' in VERSION: CLASSIFIERS.append('Development Status :: 5 - Production/Stable')
elif 'a' in VERSION: CLASSIFIERS.append('Development Status :: 3 - Alpha')
elif 'b' in VERSION: CLASSIFIERS.append('Development Status :: 4 - Beta')

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_MAIL,
    description=DESCRIPTION,
    long_description=read(README),
    url=URL,
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    packages=['djangocms_gallery', 'djangocms_gallery.migrations'],
)