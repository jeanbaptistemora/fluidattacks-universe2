# shellcheck shell=bash

function main {
      gem install \
        --no-document \
        --install-dir "${out}" \
        "${envRequirement}" \
  &&  shopt -s nullglob \
  &&  for bin in "${out}/bin/"*
      do
            sed -i "s|#!/usr/bin/env ruby|#! ${envRuby}/bin/ruby|g" "${bin}" \
        ||  return 1
      done
}

main "${@}"
