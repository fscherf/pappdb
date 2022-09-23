#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    include_package_data=True,
    name='pappdb',
    version='0.0',
    author='Florian Scherf',
    url='https://github.com/fscherf/pappdb',
    author_email='mail@florianscherf.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'prettytable~=3.4',
    ],
    scripts=[],
)
