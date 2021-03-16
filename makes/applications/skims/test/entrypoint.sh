# shellcheck shell=bash

function main {
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  local cache_local="${HOME_IMPURE}/.skims/cache"
  local cache_remote="s3://skims.data/cache/${CI_COMMIT_REF_NAME}"
  local skims_test_group="${1:-all}"

      echo '[INFO] Creating staging area' \
  &&  copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
  &&  aws_login_dev 'skims' \
  &&  aws_s3_sync "${cache_remote}" "${cache_local}" \
  &&  echo "[INFO] Running test suite with group: ${skims_test_group}" \
  &&  pushd skims \
    &&  pytest \
          --assert plain \
          --capture tee-sys \
          --disable-pytest-warnings \
          --durations 10 \
          --exitfirst \
          --reruns 10 \
          --showlocals \
          --show-capture no \
          --skims-test-group "${skims_test_group}" \
          -vvv \
  &&  popd \
  &&  echo '[INFO] Cleaning environment' \
  &&  aws_s3_sync "${cache_local}" "${cache_remote}" \
  ||  return 1
}

main "${@}"
