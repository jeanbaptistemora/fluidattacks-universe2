FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Bogota

ADD . /root/

WORKDIR /root/

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg2 \
        netbase \
        sudo \
        unzip \

    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && curl -L https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent2.sh | sh \
    && curl -LsSo vault.zip https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip \
        && unzip vault.zip \
        && mv vault /usr/local/bin \
        && rm vault.zip \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.9.0/vaultenv-0-9-0.deb \
        && dpkg -i vaultenv.deb \
        && rm vaultenv.deb \

    && apt-get update \
    && apt-get install --no-install-recommends -y \
        apache2 \
        build-essential \
        cron \
        default-libmysqlclient-dev \
        libapache2-mod-wsgi \
        libmagic1 \
        nodejs \
        python \
        python-dev \
        redis \
        ruby \

    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
        && python get-pip.py \
        && rm get-pip.py \
    && pip2 install -r requirements.txt \

    && gem install -N asciidoctor-pdf --pre \
    && /usr/sbin/td-agent-gem install eventmachine em-http-request fluent-plugin-rewrite-tag-filter \

    && cd front/ \
        && npm install \
    && cd ../assets/ \
        && npm install \
    && cd /usr/local/lib/python2.7/dist-packages/redis_sessions \
        && cat /root/enable_redis_cluster_sessions.diff | patch -p1 \

    && apt-get remove -y --purge build-essential \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && cd /root/ \
        && rm -rf \
            Dockerfile \
            enable_redis_cluster_sessions.diff \
            requirements.txt \
            /var/lib/apt/lists/*
