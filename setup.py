#!/usr/bin/env python3

from setuptools import setup, find_packages
import sys

if sys.version_info.major < 3:
    raise SystemExit("Python 3 is required!")

setup(
    name="batchprep",
    version="0.1",
    description="Prepare job batches for QC programs on SLURM clusters.",
    url="https://github.com/eljost/batchprep",
    maintainer="Johannes Steinmetzer",
    maintainer_email="johannes.steinmetzer@uni-jena.de",
    license="GPL 3",
    platforms=["unix"],
    packages=find_packages(),
    install_requires=[
        "natsort",
        "pyyaml",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "batchprep = batchprep.main:run",
        ]
    },
)
