FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git

COPY ./ /code/

ARG PROVISIONER

RUN   nix-shell --run ':' "/code/build2/provisioners/${PROVISIONER}.nix" \
  &&  nix-store --optimise
