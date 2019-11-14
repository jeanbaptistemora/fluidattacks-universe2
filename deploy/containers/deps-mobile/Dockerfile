FROM starefossen/ruby-node:2-10

# Static dependencies
RUN export \
      VAULT_URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip' \
      VAULTENV_URL='https://github.com/channable/vaultenv/releases/download/v0.11.0/vaultenv-v0.11.0-linux-musl' \
    && apt -o Acquire::Check-Valid-Until=false update \
    && apt install --no-install-recommends -y \
        openjdk-8-jdk-headless \
        rsync \
        unzip \
    && gem install bundler \
    && curl -LsSo vault.zip "${VAULT_URL}" \
      && unzip vault.zip \
      && mv vault /usr/local/bin \
      && rm vault.zip \
    && curl "$VAULTENV_URL" -LsSo /usr/local/bin/vaultenv  \
      && chmod 0755  /usr/local/bin/vaultenv

WORKDIR /usr/src/app

# Install mobile dependencies
COPY /mobile/package.json .
RUN npm install \
    && npx turtle setup:android --sdk-version 33.0.0 \
      && yes | ~/.turtle/androidDependencies/sdk/tools/bin/sdkmanager --licenses

# Apply some patches
COPY deploy/containers/deps-mobile/fix_standalone_google_login.diff /tmp
RUN patch -d node_modules/expo/build -p1 \
      < /tmp/fix_standalone_google_login.diff

# Increase max_user_watches for OTA deploys
RUN echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf \
    && sysctl -p

# Clean
RUN rm -rf /tmp/*

# Source code
COPY /mobile/* .
