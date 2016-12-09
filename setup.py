from distutils.core import setup

with open("requirements-tests.txt", 'r') as f:
    requirements = f.read().split('\n')

setup(
    name='py_proj_lights',
    version='1.0.0',
    packages=['Drawing', 'Simulation'],
    url='https://github.com/DrimTim32/py_proj_lights',
    license='',
    author='',
    author_email='',
    description='',
    install_requires=requirements
)
