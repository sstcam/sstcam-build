FROM centos:8
WORKDIR /tmp
RUN dnf -y update \
    && dnf -y install epel-release \
    && dnf -y groupinstall 'development tools' \
    && dnf -y install boost-devel cppzmq-devel protobuf git cmake python36 platform-python-devel \
    && git clone https://github.com/open62541/open62541.git \
    && cd open62541 \
    && git submodule update --init --recursive \
    && mkdir build && cd build \
    && cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DUA_NAMESPACE_ZERO=REDUCED .. \
    && make \
    && sudo make install \

