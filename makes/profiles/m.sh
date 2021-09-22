#! /bin/sh

nix-env \
  --install \
  --attr m \
  --file https://gitlab.com/fluidattacks/product/-/archive/master.tar.gz \
  --option narinfo-cache-negative-ttl 1 \
  --option narinfo-cache-positive-ttl 1
