#!/usr/bin/env bash
mkdir build
cd build
cmake -DZMQ_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=${PREFIX} ..
make -j4
make install