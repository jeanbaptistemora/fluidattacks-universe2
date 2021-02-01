# syntax=docker/dockerfile:experimental

FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

ARG PROVISIONER

RUN   --mount=type=bind,src=.,target=/code \
      nix-shell --run ':' "/code/build/provisioners/${PROVISIONER}.nix" \
  &&  nix-store --optimise
