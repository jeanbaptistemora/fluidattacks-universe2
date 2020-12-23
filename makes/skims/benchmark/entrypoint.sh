#! __envShell__
# shellcheck shell=bash

source '__makeEntrypoint__'

function main {
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  export EXPECTED_RESULTS_CSV="${benchmark_local_repo}/expectedresults-1.2.csv"
  export PRODUCED_RESULTS_CSV="${PWD}/results.csv"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  echo '[INFO] Analyzing repository' \
  &&  '__envSkims__' '__envSrcSkimsTest__/data/config/benchmark_owasp.yaml' \
  &&  echo '[INFO] Computing score' \
  &&  '__envPython__' '__envSrcSkimsSkims__/benchmark/__init__.py' \
  &&  echo '[INFO] Cleaning environment' \
  &&  remove "${PRODUCED_RESULTS_CSV}" benchmark.json \
  ||  return 1
}

main "${@}"
