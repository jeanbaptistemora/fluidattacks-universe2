# shellcheck shell=bash

function owasp {
  local category="${1:-}"
  local extra_flags=( "${@:2}" )
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  export EXPECTED_RESULTS_CSV="${benchmark_local_repo}/expectedresults-1.2.csv"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  echo '[INFO] Analyzing repository' \
  &&  rm -rf 'skims/test/outputs/'* \
  &&  if test -n "${category}"
      then
        skims "${extra_flags[@]}" "skims/test/data/config/benchmark_owasp_${category}.yaml"
      else
        for config in "skims/test/data/config/benchmark_owasp_"*".yaml"
        do
              skims "${config}" \
          ||  return 1
        done
      fi \
  &&  echo '[INFO] Computing score' \
  &&  python3.8 'skims/skims/benchmark/__init__.py' \
  ||  return 1
}

function upload {
      aws_login_prod 'observes' \
  &&  analytics_auth_redshift_file="$(mktemp)" \
  &&  sops_export_vars 'observes/secrets-prod.yaml' \
        analytics_auth_redshift \
  &&  echo "${analytics_auth_redshift}" > "${analytics_auth_redshift_file}" \
  &&  echo '[INFO] Running tap' \
  &&  observes-tap-json \
        < 'benchmark.json' \
        > '.singer' \
  &&  echo '[INFO] Running target' \
  &&  observes-target-redshift \
        --auth "${analytics_auth_redshift_file}" \
        --drop-schema \
        --schema-name 'skims_benchmark' \
        < '.singer'
}

function main {
  local category="${1:-}"
  local extra_flags=( "${@:2}" )

      owasp "${category}" "${extra_flags[@]}" \
  &&  if test -z "${category}"
      then
        upload
      fi
}

main "${@}"
