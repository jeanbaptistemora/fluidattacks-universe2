# shellcheck shell=bash

function upload {
  aws_login_prod 'observes' \
    && analytics_auth_redshift_file="$(mktemp)" \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      analytics_auth_redshift \
    && echo "${analytics_auth_redshift}" > "${analytics_auth_redshift_file}" \
    && echo '[INFO] Running tap' \
    && observes-singer-tap-json-bin \
      < 'benchmark.json' \
      > '.singer' \
    && echo '[INFO] Running target' \
    && observes-target-redshift \
      --auth "${analytics_auth_redshift_file}" \
      --drop-schema \
      --schema-name 'skims_benchmark' \
      < '.singer'
}

function main {
  local category="${1:-}"
  local extra_flags=("${@:2}")

  skims-owasp-benchmark "${category}" "${extra_flags[@]}" \
    && if test -z "${category}"; then
      upload
    fi
}

main "${@}"
