FROM debian:buster-slim

ARG NODE_URL='https://deb.nodesource.com/setup_10.x'
ARG URL_SOPS='https://github.com/mozilla/sops/releases/download/v3.5.0/sops-v3.5.0.linux'

# Apt dependencies
RUN echo 'deb http://ftp.us.debian.org/debian unstable main' \
    >> /etc/apt/sources.list \
  && mkdir -p /usr/share/man/man1 \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    curl \
    g++ \
    git \
    make \
    openjdk-8-jdk-headless \
    patch \
    procps \
    python3 \
    python3-dev \
    python3-pip \
    ruby \
    ruby-dev \
  && apt-get autoremove -y --purge \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# External dependencies
RUN curl -sL "$NODE_URL" | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && curl -LsSo sops "$URL_SOPS" \
      && chmod +x sops \
      && mv sops /usr/local/bin/ \
    && pip3 install --upgrade \
      pip \
      setuptools \
      wheel

# Python deps
RUN pip3 install \
  awscli

# Gem dependencies
COPY /mobile/Gemfile .
RUN gem install bundler \
  && bundle install

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
COPY /mobile ./

CMD ["bash"]
