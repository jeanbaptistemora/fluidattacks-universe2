FROM debian:buster-slim

ARG VAULT_URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip'
ARG VAULTENV_URL='https://github.com/channable/vaultenv/releases/download/v0.11.0/vaultenv-v0.11.0-linux-musl'

# Apt dependencies
RUN echo 'deb http://ftp.us.debian.org/debian unstable main' \
    >> /etc/apt/sources.list \
  && mkdir -p /usr/share/man/man1 \
  && apt update \
  && apt install -y \
    openjdk-8-jdk-headless \
    nodejs \
    npm \
    rsync \
    unzip \
    curl \
    procps \
    patch \
    ruby-full

# External dependencies
RUN curl -LsSo vault.zip "$VAULT_URL" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && curl "$VAULTENV_URL" -LsSo /usr/local/bin/vaultenv \
    && chmod 0755 /usr/local/bin/vaultenv

# Gem dependencies
RUN gem install bundler

WORKDIR /usr/src/app

# Npm dependencies
COPY /mobile/package.json .
RUN npm install

# Install turtle
RUN npx turtle setup:android --sdk-version 33.0.0 \
    && yes | ~/.turtle/androidDependencies/sdk/tools/bin/sdkmanager --licenses

# Apply some patches
COPY deploy/containers/deps-mobile/fix_standalone_google_login.diff /tmp
RUN patch -d node_modules/expo/build -p1 < /tmp/fix_standalone_google_login.diff

# Clean
RUN rm -rf /tmp/*

# Source code
COPY /mobile/* ./
