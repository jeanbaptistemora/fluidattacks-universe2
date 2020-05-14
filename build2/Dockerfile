FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git

ARG PROVISIONER

COPY build/ /code/build/

RUN   nix-shell --run ':' "/code/build/provisioners/${PROVISIONER}.nix" \
  &&  nix-store --optimise
