#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="pyautocad",
    packages=["pyautocad", "pyautocad.contrib"],
    version="0.2.0",
    description="AutoCAD Automation for Python",
    author="Roman Haritonov",
    author_email="reclosedev@gmail.com",
    url="https://github.com/reclosedev/pyautocad",
    install_requires=[
        'comtypes>=1.1.1',
    ],
    keywords=["autocad", "automation", "activex", "comtypes"],
    license="BSD License",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ],
    long_description=open('README.rst').read()
)
