FROM debian:stretch

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf8

RUN apt update \
    && apt dist-upgrade \
    && apt install -y \
        apt-transport-https \
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
    && curl -LsSo vault.zip https://releases.hashicorp.com/vault/1.0.2/vault_1.0.2_linux_amd64.zip \
        && unzip vault.zip \
        && mv vault /usr/local/bin \
        && rm -f vault.zip \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
        && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
        && apt update \
        && ACCEPT_EULA=Y apt-get install -y \
            msodbcsql17 \
            unixodbc-dev \
    && rm -rf /var/lib/apt
