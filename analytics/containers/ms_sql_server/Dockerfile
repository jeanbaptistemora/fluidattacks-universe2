FROM debian:stretch

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf8

RUN apt update \
    && apt dist-upgrade \
    && apt install -y \
        build-essential \
        unzip \
        curl \
        wget \
        git \
        jq \
        libncursesw5-dev \
        libreadline-dev \
        libncurses5-dev \
        libsqlite3-dev \
        liblzma-dev \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libffi-dev \
        xz-utils \
        tk-dev \
        llvm \
    && git clone --depth 1 --branch 3.7 https://github.com/python/cpython.git \
        && cd cpython \
        && ./configure \
        && make --jobs=4 build_all \
        && make --jobs=4 install \
        && cd .. \
        && rm -rf cpython \
        && python3 -m ensurepip \
        && python3 -m pip install --upgrade pip \
    && wget -O msodbcsql.deb https://packages.microsoft.com/debian/9/prod/pool/main/m/msodbcsql17/msodbcsql17_17.2.0.1-1_amd64.deb \
        && ACCEPT_EULA=Y apt install -y -f ./msodbcsql.deb \
        && apt install -y unixodbc-dev \
        && rm -f msodbcsql.deb \
    && curl -LsSo vault.zip https://releases.hashicorp.com/vault/1.0.2/vault_1.0.2_linux_amd64.zip \
        && unzip vault.zip \
        && mv vault /usr/local/bin \
        && rm -f vault.zip \
    && rm -rf /var/lib/apt
