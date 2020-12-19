#! /usr/bin/env bash

./makes/nix.sh build \
  --option 'sandbox' 'false' \
  --option 'restrict-eval' 'false' \
  --no-link \
  --show-trace \
  "${@}"
