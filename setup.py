import os
from setuptools import setup
import warnings

# from https://stackoverflow.com/a/9079062
import sys
if sys.version_info[0] < 3:
    raise Exception("micromanager only supports Python3. Did you run $python setup.py <option>.? "
                    "Try running $python3 setup.py <option>.")

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='micromanager',
    version='v0.0.1',
    description='micro-manager is a package which facilitates two-scale macro-micro coupled simulations using preCICE',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/precice/micro-manager',
    author='Ishaan Desai',
    author_email='ishaan.desai@uni-stuttgart.de',
    license='LGPL-3.0',
    packages=['micromanager'],
    install_requires=['pyprecice>=2.3.0', 'numpy>=1.13.3', 'mpi4py'],
    test_suite='tests',
    zip_safe=False)
