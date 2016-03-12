#!/usr/bin/env python
import re
from distutils.core import setup
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('ttscraper/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(name='ttscraper',
    version=version,
    description='Torrent tracker scraping library',
    long_description=long_description,
    author='notapresent@gmail.com',
    author_email='notapresent@gmail.com',
    license='Apache 2.0',
    url='https://github.com/notapresent/ttscraper',
    packages=['ttscraper']
)
