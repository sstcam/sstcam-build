from setuptools import setup, find_packages

install_requires = ["pyyaml", "pytest", "pytest-custom_exit_code","jinja2"]

setup(
    name="SST Camera Build System",
    version="0.1.0",
    description="A framework to handle the building of the SST Camera software",
    author="Samuel Flis",
    author_email="samuel.flis@desy.de",
    url="https://github.com/cta-chec/sstcam-build",
    packages=find_packages(),
    provides=["scbuild"],
    license="GNU Lesser General Public License v3 or later",
    install_requires=install_requires,
    # extras_requires={
    #     #'encryption': ['cryptography']
    # },
    package_data={"": ["root_template/**/*", "root_template/*", "conda_build/**/*", "conda_build/*"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["sc-build=scbuild.sstcambuild:main",]},
)
