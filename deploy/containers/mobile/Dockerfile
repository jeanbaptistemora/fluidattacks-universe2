FROM starefossen/ruby-node:2-10

ARG PATCHES=deploy/containers/deps
ARG VAULT_BASE=https://releases.hashicorp.com/vault
ARG VAULT_VERSION=0.11.6/vault_0.11.6_linux_amd64.zip
ARG VAULTENV_BASE=https://github.com/channable/vaultenv/releases/download
ARG VAULTENV_VERSION=v0.9.0/vaultenv-0-9-0.deb

# apt deps
RUN apt update \
  && apt install --no-install-recommends -y \
    openjdk-8-jdk-headless \
    rsync \
    unzip

# gem deps
RUN gem install bundler

# npm deps
WORKDIR /usr/src/app
COPY /mobile/package.json .
RUN npm install
COPY /mobile/* .

# install vault and vaultenv
RUN curl -LsSo vault.zip "${VAULT_BASE}/${VAULT_VERSION}" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && curl -LsSo vaultenv.deb "${VAULTENV_BASE}/${VAULTENV_VERSION}" \
    && dpkg -i vaultenv.deb \
    && rm vaultenv.deb

# Increase max_user_watches for OTA deploys
RUN echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf && sysctl -p

# install turtle
COPY "${PATCHES}/fix_standalone_google_login.diff" .
RUN npx turtle setup:android --sdk-version 33.0.0 \
  && yes | ~/.turtle/androidDependencies/sdk/tools/bin/sdkmanager --licenses \
  && cat fix_standalone_google_login.diff \
    | patch -d node_modules/expo/build -p1 \
  && rm fix_standalone_google_login.diff
