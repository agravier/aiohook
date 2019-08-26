#!/usr/bin/env python

import os
import sys

from setuptools import setup

if __name__ == "__main__":
    if sys.argv[-1] == "publish":
        os.system("python setup.py bdist_wheel upload --sign")
        sys.exit()

with open("README.md") as readme:
    setup(
        use_scm_version=True,
        long_description=readme.read())
