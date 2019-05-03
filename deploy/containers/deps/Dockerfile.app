FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Bogota

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg2 \
        netbase \
        sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && curl -L https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent2.sh | sh \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.9.0/vaultenv-0-9-0.deb \
        && dpkg -i vaultenv.deb \
        && rm vaultenv.deb \
    && rm -rf /var/lib/apt/lists/*

COPY . /root/

WORKDIR /root

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        apache2 \
        build-essential \
        cron \
        default-libmysqlclient-dev \
        git \
        libapache2-mod-wsgi \
        libmagic1 \
        libmariadb3 \
        nodejs \
        python \
        python-dev \
        redis \
        ruby \
        libpq-dev \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    && pip2 install --no-cache-dir -r requirements-app.txt \
    && gem install -N asciidoctor -v 1.5.8 \
    && gem install -N asciidoctor-pdf --pre \
    && /usr/sbin/td-agent-gem install eventmachine em-http-request fluent-plugin-rewrite-tag-filter \
    && cd front/ \
        && npm install \
        && npm cache clean --force \
    && cd ../mobile/ \
        && npm install --production \
        && npm cache clean --force \
    && cd /usr/local/lib/python2.7/dist-packages/redis_sessions \
        && cat /root/enable_redis_cluster_sessions.diff | patch -p1 \
    && apt-get remove -y --purge \
        build-essential \
        default-libmysqlclient-dev \
        lsb-release \
        python-dev \
    && apt-get -y autoremove \
    && rm -rf \
        /root/Dockerfile* \
        /root/enable_redis_cluster_sessions.diff \
        /root/requirements* \
        /var/lib/apt/lists/*
