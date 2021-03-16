# shellcheck shell=bash

function owasp {
  local category="${1:-}"
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  local cache_local="${HOME_IMPURE}/.skims/cache"
  local cache_remote="s3://skims.data/cache/owasp_benchmark"
  export EXPECTED_RESULTS_CSV="${benchmark_local_repo}/expectedresults-1.2.csv"
  export PRODUCED_RESULTS_CSV="${PWD}/results.csv"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  echo '[INFO] Analyzing repository' \
  &&  if test -n "${category}"
      then
            skims --debug "skims/test/data/config/benchmark_owasp_${category}.yaml" \
        &&  cp "skims/test/outputs/benchmark_owasp_${category}.csv" 'results.csv'
      else
            aws_login_prod 'skims' \
        &&  aws_s3_sync "${cache_remote}" "${cache_local}" \
        &&  skims 'skims/test/data/config/benchmark_owasp.yaml' \
        &&  aws_s3_sync "${cache_local}" "${cache_remote}"
      fi \
  &&  echo '[INFO] Computing score' \
  &&  python3.8 'skims/skims/benchmark/__init__.py' \
  &&  echo '[INFO] Cleaning environment' \
  &&  if test -z "${category}"
      then
            aws_login_prod 'skims' \
        &&  result_path="s3://skims.data/benchmark_result/$(date -u -Iminutes).csv" \
        &&  echo "[INFO] Uploading results to ${result_path}" \
        &&  aws s3 cp "${PRODUCED_RESULTS_CSV}" "${result_path}"
      fi \
  &&  rm -rf "${PRODUCED_RESULTS_CSV}" \
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
        < '.singer' \
  &&  rm -rf '.singer' 'benchmark.json'
}

function main {
  local category="${1:-}"

      owasp "${category}" \
  &&  if test -z "${category}"
      then
        upload
      fi
}

main "${@}"
