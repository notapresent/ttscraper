#!/usr/bin/env python
from distutils.core import setup
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='ttscraper',
    version='0.1',
    description='Torrent tracker scraping library',
    long_description=long_description,
    author='notapresent@gmail.com',
    author_email='notapresent@gmail.com',
    url='https://github.com/notapresent/ttscraper',
    packages=['ttscraper']
)
