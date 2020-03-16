FROM centos:8
WORKDIR /tmp
RUN dnf -y update \
    && dnf -y install epel-release \
    && dnf -y install 'dnf-command(config-manager)'\
    && dnf config-manager --set-enabled PowerTools \
    && dnf -y groupinstall 'development tools' \
    && dnf -y install boost-devel cppzmq-devel protobuf-devel glog-devel git cmake \
    && dnf -y install python36 platform-python-devel cfitsio-devel python3-numpy python3-pytest \
    && dnf -y install rsync python3-pyyaml 
#    && git clone https://github.com/open62541/open62541.git \
#    && cd open62541 \
#    && git submodule update --init --recursive \
#    && mkdir build && cd build \
#    && cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DUA_NAMESPACE_ZERO=REDUCED .. \
#    && make \
#    && sudo make install \

