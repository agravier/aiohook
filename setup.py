#!/usr/bin/env python
import glob
import subprocess
import sys

from setuptools import setup

if __name__ == "__main__":
    if sys.argv[-1] == "publish":
        subprocess.run(["python", "setup.py", "sdist"], check=True)
        subprocess.run(["twine", "upload"] + glob.glob("dist/*"),
                       check=True)
        sys.exit()

with open("README.md") as readme:
    setup(
        use_scm_version=True,
        long_description=readme.read())
