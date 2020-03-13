FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.2-r0

ARG PROVISIONER

COPY build/ /code/build/

COPY "build/provisioners/${PROVISIONER}.nix" /code/build/provisioners/

RUN   nix-shell --run ':' "/code/build/provisioners/${PROVISIONER}.nix" \
  &&  nix-store --optimise
