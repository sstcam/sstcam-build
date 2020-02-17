# sstcam-build
The build system for SSTCam


## Installation
For a normal install run

`python setup.py install`

or in the root directory of the project do

`pip install .`

If you are developing it is recommendended to do

`pip install -e .`

instead and adding the `--user` option if not installing in a conda env. This lets changes made to the project automatically propagate to the install without the need to reinstall.

## Usage

This package provides a small application that is used to initialize the sstcam build system by cloning the specific repositories and setting up the necessary directories. The steps to build the sstcam software are:

1. Create a directory where you want the build to take place
2. Run `sc-build init` inside the directory
3. Step into the newly created `build` directory
4. Run `cmake ..` (add appropriate cmake options as needed)
5. Run `make`, which build all the software

# Prerequisites 
- cfitsio
- pyyaml
- pytest
- numpy

