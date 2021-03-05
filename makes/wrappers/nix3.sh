#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell -I nixpkgs=https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz
#!   nix-shell -p nixFlakes
#  shellcheck shell=bash

function main {
  local experimental_features=(
    nix-command
    ca-references
    flakes
  )
  local substituters=(
    https://fluidattacks.cachix.org
    https://cache.nixos.org
  )
  local trusted_public_keys=(
    fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=
    cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
  )

  nix \
    --experimental-features "${experimental_features[*]}" \
    --option allow-dirty true \
    --option builders-use-substitutes true \
    --option cores 1 \
    --option download-attempts 1 \
    --option eval-cache false \
    --option http-connections 256 \
    --option keep-going true \
    --option max-jobs auto \
    --option narinfo-cache-negative-ttl 1 \
    --option narinfo-cache-positive-ttl 1 \
    --option restrict-eval false \
    --option sandbox false \
    --option substituters "${substituters[*]}" \
    --option trusted-public-keys "${trusted_public_keys[*]}" \
    --print-build-logs \
    --show-trace \
    --verbose \
    "${@}"
}

main "${@}"
