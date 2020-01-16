from setuptools import setup, find_packages

install_requires = ["pyyaml", ]

setup(
    name="SST Camera Build System",
    # version=package.version.get_version(pep440=True),
    description="A framework to handle the building of the SST Camera software",
    author="Samuel Flis",
    author_email="samuel.flis@desy.de",
    url="https://github.com/cta-chec/sstcam-build",
    packages=find_packages(),
    provides=["scbuild"],
    license="GNU Lesser General Public License v3 or later",
    # install_requires=install_requires,
    # extras_requires={
    #     #'encryption': ['cryptography']
    # },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "sc-build=scbuild.sstcambuild:main",
        ]
    },
)

