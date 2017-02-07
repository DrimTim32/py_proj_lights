from setuptools import setup, find_packages

with open("requirements-tests.txt", 'r') as f:
    test_requirements = f.read().split('\n')
with open("requirements.txt", 'r') as f:
    requirements = f.read().split('\n')

setup(
    name='py_proj_lights',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/DrimTim32/py_proj_lights',
    license='MIT',
    author='gese anna, sobol bartek, malinowski marcin',
    author_email='',
    description='',
    setup_requires=requirements,
    tests_require=test_requirements,
    use_2to3_exclude_fixers=['lib2to3.fixes.fix_import'],
)
