FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

COPY . /data

WORKDIR /data

ENV CI_COMMIT_REF_NAME=master

RUN ./install.sh
