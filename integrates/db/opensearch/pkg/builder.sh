# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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

function apply_patches {
  # Temporal workaround to 'convince' opensearch to run on makes containers
  # https://github.com/fluidattacks/makes/issues/944
  : \
    && mkdir -p "org/opensearch/bootstrap" \
    && cp "${envPatchedNatives}" "org/opensearch/bootstrap/Natives.class" \
    && jar -uf "${out}/lib/opensearch-1.3.0.jar" "org/opensearch/bootstrap/" \
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
    && apply_patches \
    && opensearch_keystore create \
    || return 1
}

main "${@}"
