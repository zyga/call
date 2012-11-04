#!/usr/bin/env python3
#
# Copyright 2012 Zygmunt Krynicki
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
# See COPYING for details


from setuptools import setup, find_packages

setup(
    name="call",
    version="0.1",
    packages=find_packages(),
    author="Zygmunt Krynicki",
    author_email="zygmunt.krynicki@canonical.com",
    url="https://github.com/zyga/call/",
    license="LGPL",
    test_suite='call.tests',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        ("License :: OSI Approved :: GNU Lesser General Public License v3 or"
         " later (LGPLv3+)"),
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Pure-python reimplementation of python call semantics")
