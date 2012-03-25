#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

with open('README.txt') as f:
    long_description = f.read()

setup(
    name = "pyautocad",
    packages = ["pyautocad", "pyautocad.contrib"],
    version = "0.1.1",
    description = "AutoCAD Automation for Python",
    author = "Roman Haritonov",
    author_email = "reclosedev@gmail.com",
    url = "https://bitbucket.org/reclosedev/pyautocad",
    install_requires=[
        'comtypes>=0.6.2',
    ],
    keywords = ["autocad", "automation", "activex", "comtypes"],
    license = "BSD License",
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        ],
    long_description = long_description
)
