ARG CI_COMMIT_REF_NAME

FROM registry.gitlab.com/fluidattacks/integrates/deps-production:$CI_COMMIT_REF_NAME

ARG VAULT_URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip'
ARG GECKO_DRIVER_URL='https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz'
ARG DYNAMODB_LOCAL_URL='https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz'
ARG PIP_REQUIREMENTS='deploy/containers/deps-development/requirements.txt'

# external deps
RUN curl -LsSo vault.zip "$VAULT_URL" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && curl -Lo geckodriver.tar.gz "$GECKO_DRIVER_URL" \
    && tar xzf geckodriver.tar.gz -C /usr/local/bin \
    && rm geckodriver.tar.gz \
  && curl -Lo dynamodb_local.tar.gz "$DYNAMODB_LOCAL_URL" \
    && mkdir -p /usr/local/lib/dynamodb-local \
    && tar xzf dynamodb_local.tar.gz -C /usr/local/lib/dynamodb-local \
    && rm dynamodb_local.tar.gz

# fix jre dependencies
RUN mkdir -p /usr/share/man/man1

# apt deps
RUN apt-get -o Acquire::Check-Valid-Until=false update \
  && apt-get -y upgrade \
  && apt-get install -y --no-install-recommends \
    unzip \
    libpq-dev \
    firefox-esr \
    jq \
    ruby-dev \
    wget \
    default-jre

# python deps
COPY "$PIP_REQUIREMENTS" /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# npm deps. node_modules folders are stored in /npm-deps,
# make sure to copy them to the required folder if needed.
# In this stage, production node_modules built in deps-production
# container are taken to /tmp/front. Then, development deps install
# on top of it and finally, the new node_modules is moved to
# /npm-deps again
COPY front /tmp/front
RUN mv /npm-deps/front/node_modules /tmp/front/ \
  && npm install --prefix /tmp/front --only=development \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/

# cleans
RUN rm -rf \
    /tmp/*
