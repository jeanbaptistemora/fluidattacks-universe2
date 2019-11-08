FROM debian:buster-slim

ARG CI_COMMIT_REF_NAME

ARG VAULT_URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip'
ARG VAULTENV_URL='https://github.com/channable/vaultenv/releases/download/v0.10.0/vaultenv-0.10.0_x86_64-ubuntu-1804.deb'
ARG GECKO_DRIVER_URL='https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz'
ARG DYNAMODB_LOCAL_URL='https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz'
ARG PIP_REQUIREMENTS_DEV='deploy/containers/deps-development/requirements.txt'
ARG PIP_REQUIREMENTS_PROD='deploy/containers/deps-production/requirements.txt'
ARG TERRAFORM_URL='https://releases.hashicorp.com/terraform/0.11.14/terraform_0.11.14_linux_amd64.zip'
ARG KUBECTL_URL='https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl'
ARG NODE_URL='https://deb.nodesource.com/setup_10.x'
ARG TREASUREDATA_URL='https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent2.sh'


RUN apt -o Acquire::Check-Valid-Until=false update \
  && apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    openssl
RUN mkdir -p /usr/share/man/man1 \
  && apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    unzip \
    curl \
    netbase \
    build-essential \
    ca-certificates \
    libpq-dev \
    firefox-esr \
    jq \
    ruby-dev \
    wget \
    gettext-base \
    libapache2-mod-wsgi-py3 \
    python3 \
    redis \
    python3-dev \
    python3-pip \
    default-jre \
    apache2 \
    sudo \
    libpq-dev \
    git \
    libmagic1 \
    default-libmysqlclient-dev \
    firefox-esr=60.8.0esr*

# external deps
RUN curl -LsSo vault.zip "$VAULT_URL" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && curl "$VAULTENV_URL" -LsSo vaultenv.deb  \
    && dpkg -i vaultenv.deb \
    && rm vaultenv.deb \
  && curl -Lo geckodriver.tar.gz "$GECKO_DRIVER_URL" \
    && tar xzf geckodriver.tar.gz -C /usr/local/bin \
    && rm geckodriver.tar.gz \
  && curl -Lo dynamodb_local.tar.gz "$DYNAMODB_LOCAL_URL" \
    && mkdir -p /usr/local/lib/dynamodb-local \
    && tar xzf dynamodb_local.tar.gz -C /usr/local/lib/dynamodb-local \
    && rm dynamodb_local.tar.gz \
  && curl -o terraform.zip "$TERRAFORM_URL" \
    && unzip terraform.zip \
    && rm terraform.zip \
    && mv terraform /usr/local/bin/terraform \
  && curl -o kubectl "$KUBECTL_URL" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/kubectl \
  && curl -sL "$NODE_URL" | bash - \
    && apt install -y --no-install-recommends nodejs \
  && curl -L "$TREASUREDATA_URL" | sh \
  && gem install -N asciidoctor:1.5.8 concurrent-ruby \
  && gem install -N asciidoctor-pdf:1.5.0.alpha.16 --pre \
  && /usr/sbin/td-agent-gem install \
    eventmachine \
    em-http-request \
    fluent-plugin-rewrite-tag-filter

COPY "$PIP_REQUIREMENTS_DEV" /tmp/reqs_dev.txt
COPY "$PIP_REQUIREMENTS_PROD" /tmp/reqs_prod.txt
RUN pip3 install -U setuptools \
  && pip3 install --no-cache-dir -r /tmp/reqs_prod.txt \
  && pip3 install --no-cache-dir -r /tmp/reqs_dev.txt

# npm deps. node_modules folders are stored in /npm-deps,
# make sure to copy them to the required folder if needed.
# In this stage, production node_modules built in deps-production
# container are taken to /tmp/front. Then, development deps install
# on top of it and finally, the new node_modules is moved to
# /npm-deps again

ADD front/package.json /tmp/front/package.json
RUN npm install -g secure-spreadsheet@0.1.0 \
  && mkdir -p /npm-deps/front \
  && npm install --prefix /tmp/front --only=production \
  && npm install --prefix /tmp/front --only=development \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/ \
  && apt -y autoremove \
  && rm -rf /tmp/*
