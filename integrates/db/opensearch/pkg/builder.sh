# shellcheck shell=bash

function opensearch_keystore {
  : \
    && java \
      -Dopensearch.path.home="${out}" \
      -Dopensearch.path.conf="${out}/config" \
      -Dopensearch.distribution.type="tar" \
      -classpath "${out}/lib/*:${out}/lib/tools/keystore-cli/*" \
      "org.opensearch.common.settings.KeyStoreCli" \
      "$@" \
    || return 1
}

function main {
  : \
    && mkdir -p "${out}" \
    && pushd "${envSrc}" \
    && cp \
      --recursive \
      --no-preserve=mode \
      bin config lib logs modules plugins "${out}" \
    && popd \
    && opensearch_keystore create \
    || return 1
}

main "${@}"
