FROM registry.gitlab.com/fluidattacks/integrates:production

ARG VAULT_URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip'
ARG GECKO_DRIVER_URL='https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz'
ARG PIP_REQUIREMENTS='deploy/containers/development/requirements.txt'

COPY "$PIP_REQUIREMENTS" /tmp

# external deps
RUN curl -LsSo vault.zip "$VAULT_URL" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && curl -Lo geckodriver.tar.gz "$GECKO_DRIVER_URL" \
    && tar xzf geckodriver.tar.gz -C /usr/local/bin \
    && rm geckodriver.tar.gz

# apt deps
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y --no-install-recommends \
    unzip \
    libpq-dev \
    firefox-esr \
    jq \
    ruby-dev \
    wget

# python deps
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# cleans
RUN rm -rf \
    /tmp/*
