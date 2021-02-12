#! /usr/bin/env bash

function main {
  local attributes=( skims )
  local revision="${1:-master}"
  local substituters=(
    https://fluidattacks.cachix.org
    https://cache.nixos.org
  )
  local trusted_public_keys=(
    fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=
    cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
  )

      nix-env --uninstall "${attributes[@]}" \
  &&  nix-env \
        --install "${attributes[@]}" \
        --file "https://gitlab.com/fluidattacks/product/-/archive/${revision}.tar.gz" \
        --option narinfo-cache-negative-ttl 1 \
        --option narinfo-cache-positive-ttl 1 \
        --option restrict-eval false \
        --option sandbox false \
        --option substituters "${substituters[*]}" \
        --option trusted-public-keys "${trusted_public_keys[*]}" \

}

main "${@}"

