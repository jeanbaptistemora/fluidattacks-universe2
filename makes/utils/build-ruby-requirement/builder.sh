# shellcheck shell=bash

function main {
  export NIX_SSL_CERT_FILE="${envCaCert}/etc/ssl/certs/ca-bundle.crt"

      gem install \
        --no-document \
        --install-dir "${out}" \
        "${envRequirement}" \
  &&  shopt -s nullglob \
  &&  for bin in "${out}/bin/"*
      do
            sed -i "s|#!/usr/bin/env ruby|#! $(command -v ruby)|g" "${bin}" \
        ||  return 1
      done
}

main "${@}"
