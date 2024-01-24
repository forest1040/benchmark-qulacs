FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# ENV PROJECT_DIR="/workspaces/qulacs"
# # Add build artifact to PYTHONPATH and python can find qulacs.
# # Egg file name might vary depending on qulacs and python version.
# ENV PYTHONPATH="${PROJECT_DIR}/dist:${PYTHONPATH}"
# ENV PYTHONPATH="${PROJECT_DIR}/build:${PYTHONPATH}"

RUN apt-get update \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131, which is done in Microsoft's devcontainer image.
    && apt-get purge -y imagemagick imagemagick-6-common \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    clang-format \
    cmake \
    curl \
    doxygen \
    git \
    vim \
    gdb \
    libboost-dev \
    libpython3-dev \
    manpages \
    man-db \
    pandoc \
    python3 \
    python3-distutils \
    python3-pip \
    python3-pybind11 \
    wget \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install -U pip \
    && pip install black flake8 openfermion mypy pybind11-stubgen

# pybind11
RUN git clone https://github.com/pybind/pybind11.git /tmp/pybind11 \
    && cd /tmp/pybind11 \
    && mkdir build && cd build \
    && cmake .. -DPYBIND11_TEST=Off \
    && make install
