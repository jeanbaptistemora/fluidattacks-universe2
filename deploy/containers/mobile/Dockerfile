FROM starefossen/ruby-node:2-10

ARG PATCHES=deploy/containers/deps

# apt deps
RUN apt update \
  && apt install --no-install-recommends -y \
    openjdk-8-jdk-headless \
    rsync

# gem deps
RUN gem install bundler

# npm deps
WORKDIR /usr/src/app
COPY /mobile/package.json .
RUN npm install
COPY /mobile/* .

# install turtle
COPY "${PATCHES}/fix_standalone_google_login.diff" .
RUN npx turtle setup:android --sdk-version 33.0.0 \
  && yes | ~/.turtle/androidDependencies/sdk/tools/bin/sdkmanager --licenses \
  && cat fix_standalone_google_login.diff \
    | patch -d node_modules/expo/build -p1 \
  && rm fix_standalone_google_login.diff
