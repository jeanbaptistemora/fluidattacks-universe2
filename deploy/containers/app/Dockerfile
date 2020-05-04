FROM debian:buster-slim

ARG PATCHES='deploy/containers/app'
ARG PIP_REQUIREMENTS='deploy/containers/app/requirements.txt'
ARG PIP_REQUIREMENTS_PROD_LOCAL='deploy/containers/app/requirements_local_async.txt'
ARG DYNAMODB_LOCAL_URL='https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz'
ARG TREASUREDATA_URL='https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent3.sh'
ARG URL_SOPS='https://github.com/mozilla/sops/releases/download/v3.5.0/sops-v3.5.0.linux'

ENV DEBIAN_FRONTEND='noninteractive'
ENV TZ='America/Bogota'

LABEL mantainer='engineering@fluidattacks.com'

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
    nodejs \
    npm \
    libmagic1 \
    ruby \
    ruby-dev \
    libpq-dev \
    zip \
    jq

# external deps
RUN curl -L "$TREASUREDATA_URL" | sh \
  && gem install -N asciidoctor:2.0.10 concurrent-ruby \
  && gem install -N asciidoctor-pdf:1.5.0.rc.3 --pre \
  && /usr/sbin/td-agent-gem install \
    eventmachine \
    em-http-request \
    fluent-plugin-rewrite-tag-filter \
  && pip3 install -U setuptools==41.4.0 \
  && apt -y autoremove \
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

COPY "$PIP_REQUIREMENTS" /tmp
COPY "$PATCHES/enable_redis_cluster_sessions.diff" /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt \
  && cat /tmp/enable_redis_cluster_sessions.diff \
    | patch -d /usr/local/lib/python3.7/dist-packages/redis_sessions -p1

# npm deps. node_modules folders are stored in /npm-deps
# make sure to copy them to the required folder if needed.
COPY front /tmp/front
RUN npm install -g secure-spreadsheet@0.1.0 \
  && mkdir -p /npm-deps/front \
  && npm install --prefix /tmp/front --only=production \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/

WORKDIR /usr/src/app

ARG CI_API_V4_URL
ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_ID
ARG SSL_CERT
ARG SSL_KEY
ARG VERSION

ENV CI_COMMIT_REF_NAME $CI_COMMIT_REF_NAME
ENV FI_VERSION $VERSION

# Put integrates in container
COPY . .
RUN pip3 install --no-cache-dir --no-index \
      --find-links=django-apps/packages/ \
      --requirement deploy/containers/app/requirements_local_async.txt \
  && rm -rf /var/www/html \
  && rm -f /etc/td-agent/td-agent.conf \
  && rm -f /etc/init.d/td-agent \
  && mv deploy/containers/common/vars/fluent.conf /etc/td-agent/td-agent.conf \
  && mv deploy/containers/common/vars/td-agent /etc/init.d/td-agent \
    && chmod 0755 /etc/init.d/td-agent \
  && mv deploy/containers/common/vars/out_rollbar.rb /etc/td-agent/plugin/ \
  && mkdir app/documentator/images \
  && mkdir app/documentator/tpls \
  && mkdir app/documentator/results \
  && mkdir app/techdoc/results \
  && echo "$SSL_CERT" | base64 -di > /etc/ssl/certs/fluidla.crt \
  && echo "$SSL_KEY" | base64 -di > /etc/ssl/private/fluidla.key \
  && apt -y autoremove \
  && rm -rf /tmp/*

EXPOSE 80 24224

# Start integrates
CMD ./deploy/containers/common/vars/run.sh
