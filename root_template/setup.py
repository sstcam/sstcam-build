###########################################
#### Do not edit this file ################
#### It has been auto-generated ###########
###########################################
from setuptools import setup, find_packages
import os
import sys

install_requires = ["numpy"]

setup(
    name="sstcam",
    version="0.1.0",
    description="The SSTCAM software python package.",
    # author="Samuel Flis",
    # author_email="samuel.d.flis@gmail.com",
    # url="https://github.com/sflis/pyicf",
    packages=find_packages(),
    provides=["sstcam"],
    license="GNU Lesser General Public License v3 or later",
    install_requires=install_requires,
    # package_dir = {"sstcam": "python/sstcam"},
    package_data = {
        '': ['_ext/*']
      },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # entry_points={
    #     "console_scripts": [
    #     ]
    # },
)