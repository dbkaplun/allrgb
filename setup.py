#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements

setup(
  name='allrgb',
  version='1.0.0',
  description="Generates an image with every RGB color exactly once",
  author="Dan Kaplun",
  author_email='min@dvir.us',
  url='http://github.com/dbkaplun/allrgb',
  scripts=['allrgb.py'],
  install_requires=[str(req.req) for req in parse_requirements('requirements.txt')]
)
