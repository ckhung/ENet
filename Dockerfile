FROM ckhung/cvbstnpy:latest

LABEL maintener="Chao-Kuei Hung <ckhung@cyut.edu.tw>"

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler

WORKDIR /usr/local/lib/python3.5
RUN ln -s site-packages dist-packages

WORKDIR /
RUN git clone --recursive https://github.com/ckhung/ENet.git

WORKDIR /ENet/caffe-enet
RUN cp ../caffe-Makefile.config Makefile.config
RUN make 
RUN make pycaffe

ENV CAFFE_PATH="/ENet/caffe-enet"
ENV PYTHONPATH="$CAFFE_PATH/python:$PYTHONPATH"

RUN pip install scikit-image google protobuf

WORKDIR /ENet
RUN sh enet_weights_zoo/cityscapes_weights.sh

