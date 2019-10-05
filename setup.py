#! /usr/bin/env python3

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    return open(os.path.join(here, fname)).read()

with open(os.path.join(here, "yaqd_rpi_gpio", "VERSION")) as version_file:
    version = version_file.read().strip()

extra_files = {"yaqd_thorlabs": ["VERSION"]}

setup(
    name="yaqd_rpi_gpio",
    packages=find_packages(),
    package_data=extra_files,
    python_requires=">=3.7",
    install_requires=["yaqd-core"],
    extras_require={
        "dev": ["black", "pre-commit"],
    },
    version=version,
    description="yaq daemon for control of Rasperry Pi GPIO",
    author="yaq Developers",
    license="LGPL v3",
    url="https://gitlab.com/yaq/yaqd-rpi-gpio",
    keywords="yaq hardware",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
    ],
)
