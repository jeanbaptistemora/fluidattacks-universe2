# shellcheck shell=bash

source '__envSetupSkimsRuntime__'
source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function owasp {
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  local cache_local="${HOME}/.skims"
  local cache_remote="s3://skims.data/cache/owasp_benchmark"
  export EXPECTED_RESULTS_CSV="${benchmark_local_repo}/expectedresults-1.2.csv"
  export PRODUCED_RESULTS_CSV="${PWD}/results.csv"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  aws_login_prod 'skims' \
  &&  aws_s3_sync "${cache_remote}" "${cache_local}" \
  &&  echo '[INFO] Analyzing repository' \
  &&  '__envSkims__' '__envSrcSkimsTest__/data/config/benchmark_owasp.yaml' \
  &&  echo '[INFO] Computing score' \
  &&  '__envPython__' '__envSrcSkimsSkims__/benchmark/__init__.py' \
  &&  echo '[INFO] Cleaning environment' \
  &&  aws_s3_sync "${cache_local}" "${cache_remote}" \
  &&  remove "${PRODUCED_RESULTS_CSV}" \
  ||  return 1
}

function upload {
      aws_login_prod 'observes' \
  &&  analytics_auth_redshift_file="$(mktemp)" \
  &&  sops_export_vars 'observes/secrets-prod.yaml' 'default' \
        analytics_auth_redshift \
  &&  echo "${analytics_auth_redshift}" > "${analytics_auth_redshift_file}" \
  &&  echo '[INFO] Running tap' \
  &&  '__envTapJson__' \
        < 'benchmark.json' \
        > '.singer' \
  &&  echo '[INFO] Running target' \
  && '__envTargetRedshift__' \
        --auth "${analytics_auth_redshift_file}" \
        --drop-schema \
        --schema-name 'skims_benchmark' \
        < '.singer' \
  &&  remove '.singer' 'benchmark.json'
}

function main {
      owasp \
  &&  upload
}

main "${@}"
