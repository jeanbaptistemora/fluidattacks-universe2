#! /usr/bin/env bash

./makes/nix.sh build \
  --option 'sandbox' 'false' \
  --option 'restrict-eval' 'false' \
  --no-link \
  --no-update-lock-file \
  --show-trace \
  "${@}"
