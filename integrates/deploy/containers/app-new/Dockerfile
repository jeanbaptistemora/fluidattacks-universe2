FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

WORKDIR /usr/src/app

ARG PROVISIONER='build/provisioners/integrates_serve_back_dev.nix'
COPY . .
RUN     nix-shell --run ':' "${PROVISIONER}" \
    &&  nix-store --optimise

ENV FI_VERSION ${VERSION}
