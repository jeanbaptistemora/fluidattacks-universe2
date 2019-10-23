FROM debian:buster-slim

ARG PATCHES='deploy/containers/deps-production'
ARG NODE_URL='https://deb.nodesource.com/setup_10.x'
ARG VAULTENV_URL='https://github.com/channable/vaultenv/releases/download/v0.9.0/vaultenv-0-9-0.deb'
ARG TREASUREDATA_URL='https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent2.sh'
ARG PIP_REQUIREMENTS='deploy/containers/deps-production/requirements.txt'

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Bogota

# apt deps: Timezone and openssl first
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
  && apt -o Acquire::Check-Valid-Until=false update \
  && apt -y upgrade \
  && apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    openssl

# apt deps: Install other deps
RUN apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    ca-certificates \
    curl \
    gnupg2 \
    netbase \
    build-essential \
    default-libmysqlclient-dev \
    git \
    libmariadb3 \
    python3 \
    python3-dev \
    python3-pip \
    redis \
    sudo \
    apache2 \
    cron \
    netbase \
    libapache2-mod-wsgi-py3 \
    libmagic1 \
    ruby \
    libpq-dev

# external deps
RUN curl -sL "$NODE_URL" | bash - \
    && apt install -y --no-install-recommends nodejs \
  && curl -L "$TREASUREDATA_URL" | sh \
  && curl "$VAULTENV_URL" -LsSo vaultenv.deb  \
    && dpkg -i vaultenv.deb \
    && rm vaultenv.deb

# python deps
COPY "$PIP_REQUIREMENTS" /tmp
RUN pip3 install -U setuptools && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt

# ruby deps
RUN gem install -N asciidoctor:1.5.8 \
  && gem install -N asciidoctor-pdf:1.5.0.alpha.16 --pre \
  && /usr/sbin/td-agent-gem install \
    eventmachine \
    em-http-request \
    fluent-plugin-rewrite-tag-filter

# npm deps. node_modules folders are stored in /npm-deps
# make sure to copy them to the required folder if needed.
COPY front /tmp/front
RUN npm install -g secure-spreadsheet@0.1.0 \
  && mkdir -p /npm-deps/front \
  && npm install --prefix /tmp/front --only=production \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/

# patches and cleans
COPY "$PATCHES/enable_redis_cluster_sessions.diff" /tmp
RUN cat /tmp/enable_redis_cluster_sessions.diff \
    | patch -d /usr/local/lib/python3.7/dist-packages/redis_sessions -p1 \
  && apt -y autoremove \
  && rm -rf \
    /var/lib/apt/lists/* \
    /tmp/*
