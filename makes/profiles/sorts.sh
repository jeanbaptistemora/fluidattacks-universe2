#! /usr/bin/env bash

function main {
  local attributes=( sorts )
  local revision="${1:-master}"
  local substituters=(
    # Order matters, caches are looked-up from top to bottom
    https://fluidattacks.cachix.org
    https://cache.nixos.org
  )
  local trusted_public_keys=(
    fluidattacks.cachix.org-1:zHq9yBCfg0wUPBDWdMFs62x6X/MJvSgGAWX8Vq9PnUY
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

