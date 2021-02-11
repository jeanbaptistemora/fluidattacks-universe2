#! /usr/bin/env bash

function main {
  local attributes=( __envPackages__ )

      nix-env --uninstall "${attributes[@]}" \
  &&  nix-env \
        --install "${attributes[@]}" \
        --file 'https://gitlab.com/fluidattacks/product/-/archive/master.tar.gz' \
        --option sandbox false \
        --option restrict-eval false \
        --option narinfo-cache-negative-ttl 1 \
        --option narinfo-cache-positive-ttl 1 \

}

main
