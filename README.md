docker build -t sstcam:latest sstcam-build/# sstcam-build
The build system for SSTCam

## Docker setup

1. Define a workspace directory (`WORKSPACE_DIR` in the following), create it and cd into it.

2. Clone the sstcam-build repository, cd into it and create a docker image named sstcam:

`docker build -t sstcam:latest sstcam-build`

3. Run docker iteractively exporting the workspace directory:

`docker run -it -v ${WORKSPACE_DIR}:/workspace -w /workspace sstcam bash` 

## Installation
For a normal install run

`python setup.py install`

or in the root directory of the project do

`pip3 install .`

If you are developing it is recommendended to do

`pip3 install -e .`

instead and adding the `--user` option if not installing in a conda env. This lets changes made to the project automatically propagate to the install without the need to reinstall.

## Usage

This package provides a small application that is used to initialize the sstcam build system by cloning the specific repositories and setting up the necessary directories. The steps to build the sstcam software are:

1. Inside the `WORKSPACE_DIR`, create a directory where you want the source files to be (`SOURCE_DIR`)
2. Run `sc-build init` inside the directory
3. Step into the newly created `build` directory
4. Run `cmake ..` (add appropriate cmake options as needed)
5. Run `make`, which build all the software

# Prerequisites 
- cfitsio
- pyyaml
- pytest
- numpy

