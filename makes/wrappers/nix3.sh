#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/cb52887c38ef47f6649a21336cfaa347cc7dfa75.tar.gz
#!   nix-shell -p nixFlakes
#  shellcheck shell=bash

function main {
  local experimental_features=(
    nix-command
    ca-references
    flakes
  )
  local substituters=(
    # Order matters, caches are looked-up from top to bottom
    https://fluidattacks.cachix.org
    https://cache.nixos.org
  )
  local trusted_public_keys=(
    fluidattacks.cachix.org-1:zHq9yBCfg0wUPBDWdMFs62x6X/MJvSgGAWX8Vq9PnUY
    cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
  )

  # Missindented on purpose
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
