# shellcheck shell=bash

source '__envSetupSkimsRuntime__'
source '__envSetupSkimsDevelopment__'
source '__envUtilsBashLibAws__'

function main {
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  local cache_local="${HOME}/.skims"
  local cache_remote="s3://skims.data/cache/owasp_benchmark"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  aws_login_dev 'skims' \
  &&  aws_s3_sync "${cache_remote}" "${cache_local}" \
  &&  echo '[INFO] Testing' \
  &&  pushd 'skims' \
    &&  pytest \
          --capture tee-sys \
          --disable-pytest-warnings \
          --exitfirst \
          --reruns 10 \
          --show-capture no \
          --verbose \
          --verbose \
          --verbose \
        < /dev/null \
  &&  popd \
  &&  echo '[INFO] Cleaning environment' \
  &&  aws_s3_sync "${cache_local}" "${cache_remote}" \
  ||  return 1
}

main "${@}"
