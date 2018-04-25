# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='genetic_algorithms',
    version='0.1.0',
    description='A module for constructing genetic algorithms',
    long_description=readme,
    author='Toby Devlin',
    author_email='',
    url='',
    packages=['genetic_algorithms']
)
