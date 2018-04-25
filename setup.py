# -*- coding: utf-8 -*-

# Structure from: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='genetic-algorithms',
    version='0.1.0',
    description='A module for constructing genetic algorithms',
    long_description=readme,
    author='Toby Devlin',
    author_email='',
    url='',
    license=license,
    packages=find_packages(exclude=('test', 'docs'))
)
