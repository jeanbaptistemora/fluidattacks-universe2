FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

ARG PROVISIONER

COPY build       /code/build
COPY ci-scripts  /code/ci-scripts
COPY deploy      /code/deploy
COPY django-apps /code/django-apps

RUN   nix-shell --run ':' "/code/build/provisioners/${PROVISIONER}.nix" \
  &&  nix-store --optimise
