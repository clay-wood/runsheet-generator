#!/usr/bin/env python

from setuptools import setup

setup(name='runsheetGen', 
    version='0.1',
    author='Clay Wood',   
    packages=['runsheetGen', 
        'runsheetGen.test'],
    scripts=['runsheetGen/scripts/runsheetGen.py', 'runsheetGen/scripts/constructRunsheet.py'],
    # url='http://pypi.python.org/pypi/runsheetGen/',
    package_data={'runsheetGen': ['templates/runsheetTemplate.tex']},
    install_requires=[
        "pandas==1.3.3",
        "numpy==1.20.0",
    ],
)