FROM debian:buster-slim

ARG NODE_URL='https://deb.nodesource.com/setup_10.x'

# Apt dependencies
RUN echo 'deb http://ftp.us.debian.org/debian unstable main' \
    >> /etc/apt/sources.list \
  && mkdir -p /usr/share/man/man1 \
  && apt update \
  && apt install -y \
    openjdk-8-jdk-headless \
    rsync \
    unzip \
    curl \
    procps \
    patch \
    ruby-full

# External dependencies
RUN curl -sL "$NODE_URL" | bash - \
    && apt install -y --no-install-recommends nodejs

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
