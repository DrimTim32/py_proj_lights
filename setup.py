from setuptools import setup, find_packages

import unittest

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

with open("requirements-tests.txt", 'r') as f:
    requirements = f.read().split('\n')

setup(
    name='py_proj_lights',
    version='1.0',
    packages= find_packages(),
    url='',
    license='',
    author='',
    author_email='',
    description='',
    test_suite=my_test_suite(),
    tests_require=['pytest']
)
