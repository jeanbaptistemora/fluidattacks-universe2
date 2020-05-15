FROM nixos/nix:2.3

ARG NIXPKGS_ALLOW_UNFREE='1'
ARG PROVISIONER

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git

COPY ./ /code/

RUN   nix-shell --run ':' "/code/build2/provisioners/${PROVISIONER}.nix" \
  &&  nix-store --optimise
