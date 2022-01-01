#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='runsheetGen', 
    version='0.1.1',
    author='Clay Wood',   
    packages=['runsheetGen', 
        'runsheetGen.test'],
    scripts=['runsheetGen/scripts/runsheetGen.py', 'runsheetGen/scripts/constructRunsheet.py'],
    # url='http://pypi.python.org/pypi/runsheetGen/',
    package_data={'runsheetGen': ['templates/runsheetTemplate.tex']},
    install_requires=[
        "pandas >= 1.1.1",
        "numpy >= 1.10.0",
    ],
)
