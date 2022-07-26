# development env

ARG VERSION=3.10-bullseye
FROM python:$VERSION
ARG VERSION

LABEL maintainer "srz_zumix <https://github.com/srz-zumix>"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update -q -y && \
    apt-get install -y --no-install-recommends \
        make \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.pyenv/bin:${PATH}"
RUN curl https://pyenv.run | bash && \
    echo "eval $(pyenv init -)" >> ~/.bashrc && \
    echo "eval $(pyenv virtualenv-init -)" >> ~/.bashrc
RUN pyenv install -s "$(pyenv install -l | grep -v 'dev' | grep -e '\s3\.11[^0-9].*' | tail -1 | xargs echo -n)"
RUN pyenv install -s "$(pyenv install -l | grep -v 'dev' | grep -e '\s3\.10[^0-9].*' | tail -1 | xargs echo -n)"
RUN	pyenv install -s "$(pyenv install -l | grep -e '\s3\.9[^0-9].*' | tail -1 | xargs echo -n)"
RUN	pyenv install -s "$(pyenv install -l | grep -e '\s3\.8[^0-9].*' | tail -1 | xargs echo -n)"
RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.7[^0-9].*' | tail -1 | xargs echo -n)"
RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.6[^0-9].*' | tail -1 | xargs echo -n)"
RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.5[^0-9].*' | tail -1 | xargs echo -n)"
# RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.4[^0-9].*' | tail -1 | xargs echo -n)"
# RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.3[^0-9].*' | tail -1 | xargs echo -n)"
# RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.2[^0-9].*' | tail -1 | xargs echo -n)"
# RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.1[^0-9].*' | tail -1 | xargs echo -n)"
# RUN pyenv install -s "$(pyenv install -l | grep -e '\s3\.0[^0-9].*' | tail -1 | xargs echo -n)"
