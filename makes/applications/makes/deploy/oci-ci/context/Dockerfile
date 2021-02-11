# syntax=docker/dockerfile:experimental

FROM nixos/nix:2.3.6

# Basic dependencies in the host needed to execute ./make
RUN apk add --no-cache \
      bash=5.0.17-r0 \
      git=2.26.2-r0

# SSH Configuration
RUN mkdir -p ~/.ssh \
  &&  echo 'Host *' > ~/.ssh/config \
  &&  echo '  StrictHostKeyChecking no' >> ~/.ssh/config \
  &&  chmod 400 ~/.ssh/config
