ARG BASE_IMAGE=nvidia/cuda:11.0-runtime-ubuntu20.04
FROM ${BASE_IMAGE}
ENV DEBIAN_FRONTEND="noninteractive"
#----------------------------------------
# Install latest python3.8 + pip3 and make them default
#----------------------------------------
RUN apt update \
    && apt install -y --no-install-recommends software-properties-common \
    && add-apt-repository --yes ppa:deadsnakes/ppa \
    && apt update \
    && apt install --no-install-recommends -y python3.8 python3.8-dev python3-pip \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

#----------------------------------------
# Install some ubuntu stuff (gcc, make, etc.)
#----------------------------------------
RUN apt install -y --no-install-recommends \
    bash \
    build-essential \
    libc6-dev \
    apt-utils \
    ca-certificates \
    htop \
    wget \
    git \
    vim \
    libssl-dev \
    curl \
    unzip \
    unrar \
    aria2 \
    pbzip2 \
    pigz \
    cmake \
    libboost-all-dev
    
SHELL ["/bin/bash", "-c"]

#----------------------------------------
# Install python libs and stuff
#----------------------------------------
RUN python -m pip --no-cache-dir install --upgrade \
    pip \
    setuptools && \
    python -m pip --no-cache-dir install --upgrade \
    numpy \
    scipy \
    pandas \
    pyarrow \
    numba \
    cloudpickle \
    scikit-learn \
    matplotlib \
    Cython \
    jupyter \
    jupyterlab

#----------------------------------------
# Install prerequrements
#----------------------------------------
RUN apt install -y liblapacke-dev libsuitesparse-dev openssh-client

#----------------------------------------
# Install pytorch, jax, haiku, trax and nlp libraries

# Pytorch
ARG PYTORCH_PACKAGE=torch
RUN python -m pip --no-cache-dir install --upgrade $PYTORCH_PACKAGE

# Google's JAX
ARG JAX_PACKAGE=https://storage.googleapis.com/jax-releases/cuda110/jaxlib-0.1.52-cp38-none-manylinux2010_x86_64.whl
RUN python -m pip --no-cache-dir install --upgrade $JAX_PACKAGE

# Other packages
RUN python -m pip --no-cache-dir install --upgrade \
    jax \
    transformers nlp \
    pytorch_lightning

#----------------------------------------
# Copying tf install script
#----------------------------------------
ARG TF_FILE=install_tf2.4.0.sh
COPY docker/${TF_FILE} /workspace

#----------------------------------------
# Install better shell
#----------------------------------------
RUN apt install -y bash && \
    chsh -s /bin/bash root && \
    wget -O ~/install.sh https://starship.rs/install.sh && \
    bash ~/install.sh -y && \
    echo 'eval "$(starship init bash)"' >> ~/.bashrc

#---------------------------------------
# Installing nodejs via nvm and configuring jupyterlab, default password: 'change-me-asap'
#---------------------------------------
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 14.10.1
RUN mkdir -p $NVM_DIR && wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash && \
    source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm use $NODE_VERSION
ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN jupyter notebook --generate-config && \
    pip install ipywidgets && \ 
    jupyter nbextension enable --py widgetsnbextension && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    
#---------------------------------------
# Installing rust jupyter kernel
#---------------------------------------
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH
RUN URL="https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init" && \
    wget "$URL" && \
    chmod +x rustup-init && \
    ./rustup-init -y --no-modify-path --default-toolchain nightly && \
    rm rustup-init && \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME && \
    cargo install evcxr_jupyter && \
    evcxr_jupyter --install
    
#---------------------------------------
# Cleanup
#---------------------------------------
RUN ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/* && \
    rm -rf  ~/install.sh 

#---------------------------------------
# Finalizing
#---------------------------------------
RUN mkdir /workspace
COPY docker/hashpwd.py /workspace
RUN mkdir -p /workspace/notebooks && mkdir -p /workspace/data && python /workspace/hashpwd.py --password="change-me-asap"
WORKDIR /workspace

EXPOSE 8888 6006

CMD export SHELL=/bin/bash && jupyter notebook --no-browser --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir='/workspace'
