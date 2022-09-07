# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function upload {
  aws_login "prod_observes" "3600" \
    && db_creds="$(mktemp)" \
    && json_db_creds "${db_creds}" \
    && echo '[INFO] Running tap' \
    && observes-singer-tap-json-bin \
      < 'benchmark.json' \
      > '.singer' \
    && echo '[INFO] Running target' \
    && observes-target-redshift \
      --auth "${db_creds}" \
      --drop-schema \
      --schema-name 'skims_benchmark' \
      < '.singer'
}

function main {
  local category="${1:-}"
  local extra_flags=("${@:2}")

  skims-benchmark-owasp "${category}" "${extra_flags[@]}" \
    && if test -z "${category}"; then
      upload
    fi
}

main "${@}"
