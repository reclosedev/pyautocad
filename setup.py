#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="pyautocad",
    packages=["pyautocad", "pyautocad.contrib"],
    version="0.1.2",
    description="AutoCAD Automation for Python",
    author="Roman Haritonov",
    author_email="reclosedev@gmail.com",
    url="https://github.com/reclosedev/pyautocad",
    install_requires=[
        'comtypes',
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
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        ],
    long_description=open('README.rst').read()
)
