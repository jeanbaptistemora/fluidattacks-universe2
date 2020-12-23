#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'
source '__envUtilsBashLibSkimsAws__'

function main {
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  local cache_local="${HOME}/.skims"
  local cache_remote="s3://skims.data/cache/owasp_benchmark"
  export EXPECTED_RESULTS_CSV="${benchmark_local_repo}/expectedresults-1.2.csv"
  export PRODUCED_RESULTS_CSV="${PWD}/results.csv"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  skims_aws_login_prod \
  &&  skims_cache_pull "${cache_local}" "${cache_remote}" \
  &&  echo '[INFO] Analyzing repository' \
  &&  '__envSkims__' '__envSrcSkimsTest__/data/config/benchmark_owasp.yaml' \
  &&  echo '[INFO] Computing score' \
  &&  '__envPython__' '__envSrcSkimsSkims__/benchmark/__init__.py' \
  &&  echo '[INFO] Cleaning environment' \
  &&  skims_cache_push "${cache_local}" "${cache_remote}" \
  &&  remove "${PRODUCED_RESULTS_CSV}" benchmark.json \
  ||  return 1
}

main "${@}"
