# shellcheck shell=bash

function upload {
  aws_login_prod 'observes' \
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
