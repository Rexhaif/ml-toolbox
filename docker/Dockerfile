ARG BASE_IMAGE=nvidia/cuda:11.0-runtime-ubuntu20.04
FROM ${BASE_IMAGE}
ENV DEBIAN_FRONTEND="noninteractive"
#----------------------------------------
# Install python3.8 + pip3 and make them default
#----------------------------------------
RUN apt update && apt install --no-install-recommends -y python3.8 python3.8-dev python3-pip \
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
    pigz

#----------------------------------------
# Install cmake & boost
#----------------------------------------
RUN git clone --depth 10 https://github.com/Kitware/CMake ~/cmake && \
    cd ~/cmake && \
    ./bootstrap && \
    make -j"$(nproc)" install
RUN wget -O ~/boost.tar.gz https://dl.bintray.com/boostorg/release/1.74.0/source/boost_1_74_0.tar.gz && \
    tar -zxf ~/boost.tar.gz -C ~ && \
    cd ~/boost_* && \
    ./bootstrap.sh --with-python=/usr/local/bin/python3 --with-python-version=3.8 --with-python-root=/usr/local/lib/python3.8 && \
    ./b2 install -j"$(nproc)" --prefix=/usr/local

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
# Install pytorch, tensorflow, jax, haiku, trax and nlp libraries
#----------------------------------------
# Pytorch
ARG PYTORCH_PACKAGE=torch
RUN python -m pip --no-cache-dir install --upgrade $PYTORCH_PACKAGE

# Tensorflow
ARG TF_PACKAGE=tensorflow
RUN python -m pip --no-cache-dir install --upgrade $TF_PACKAGE

# Google's JAX
ARG JAX_PACKAGE=https://storage.googleapis.com/jax-releases/cuda110/jaxlib-0.1.52-cp38-none-manylinux2010_x86_64.whl
RUN python -m pip --no-cache-dir install --upgrade $JAX_PACKAGE

# Other packages
RUN python -m pip --no-cache-dir install --upgrade \
    jax \
    transformers nlp \
    pytorch_lightning

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
RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
RUN nvm install 14 && nvm use 14
RUN jupyter notebook --generate-config && \
    pip install ipywidgets && \ 
    jupyter nbextension enable --py widgetsnbextension && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    echo "c.NotebookApp.password = 'sha1:e38cb960008a:2d7c7b65a110ab5b94b3e4a8c98a8c274c9387a2'" > ~/.jupyter/jupyter_notebook_config.py
    
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
    rm -rf ~/boost* ~/install.sh 

#---------------------------------------
# Finalizing
#---------------------------------------
RUN mkdir -p /workspace/notebooks && mkdir -p /workspace/data
WORKDIR /workspace

EXPOSE 6006 8888

CMD export SHELL=/bin/bash && jupyter notebook --no-browser --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir='/workspace'
