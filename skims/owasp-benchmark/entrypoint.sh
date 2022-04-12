# shellcheck shell=bash

function score {
  local category="${1:-}"
  local extra_flags=("${@:2}")
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  export EXPECTED_RESULTS_CSV="${benchmark_local_repo}/expectedresults-1.2.csv"

  echo '[INFO] Creating staging area' \
    && copy '__argBenchmarkRepo__' "${benchmark_local_repo}" \
    && echo '[INFO] Analyzing repository' \
    && rm -rf 'skims/test/outputs/'* \
    && if test -n "${category}"; then
      skims scan "${extra_flags[@]}" "skims/test/data/config/benchmark_owasp_${category}.yaml"
    else
      for config in "skims/test/data/config/benchmark_owasp_"*".yaml"; do
        skims scan "${config}" \
          || return 1
      done
    fi \
    && echo '[INFO] Computing score' \
    && python3.8 'skims/skims/benchmark/__init__.py' \
    || return 1
}

function main {
  local category="${1:-}"
  local extra_flags=("${@:2}")

  score "${category}" "${extra_flags[@]}"
}

main "${@}"
