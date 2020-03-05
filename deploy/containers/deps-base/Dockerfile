FROM debian:buster-slim

ARG DYNAMODB_LOCAL_URL='https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz'
ARG NODE_URL='https://deb.nodesource.com/setup_10.x'
ARG TREASUREDATA_URL='https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent3.sh'
ARG URL_SOPS='https://github.com/mozilla/sops/releases/download/v3.5.0/sops-v3.5.0.linux'

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Bogota

# apt deps: Timezone and openssl first
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
  && apt -o Acquire::Check-Valid-Until=false update \
  && apt -y upgrade \
  && apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    openssl

# apt deps: Man pages directory
RUN mkdir -p /usr/share/man/man1

# apt deps: Install other deps
RUN apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    ca-certificates \
    default-jre \
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
    python3-venv \
    redis \
    sudo \
    cron \
    libmagic1 \
    ruby \
    ruby-dev \
    libpq-dev \
    zip \
    jq

# external deps
RUN curl -sL "$NODE_URL" | bash - \
    && apt install -y --no-install-recommends nodejs \
  && curl -L "$TREASUREDATA_URL" | sh \
  && gem install -N asciidoctor:2.0.10 concurrent-ruby \
  && gem install -N asciidoctor-pdf:1.5.0.rc.3 --pre \
  && /usr/sbin/td-agent-gem install \
    eventmachine \
    em-http-request \
    fluent-plugin-rewrite-tag-filter \
  && pip3 install -U setuptools==41.4.0 \
  && apt -y autoremove \
  && rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
  && curl -LsSo sops "$URL_SOPS" \
    && chmod +x sops \
    && mv sops /usr/local/bin/

# Python deps
RUN pip3 install \
  awscli \
  yq

# DynamoDB local for ephemeral environments
RUN curl -Lo dynamodb_local.tar.gz "$DYNAMODB_LOCAL_URL" \
    && mkdir -p /usr/local/lib/dynamodb-local \
    && tar xzf dynamodb_local.tar.gz -C /usr/local/lib/dynamodb-local \
    && rm dynamodb_local.tar.gz

CMD ["bash"]
