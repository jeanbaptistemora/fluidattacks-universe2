# shellcheck shell=bash

function main {
  local androguard_local_repo="${PWD}/../androguard"
  local benchmark_local_repo="${PWD}/../owasp_benchmark"
  local nisttestsuites_local_repo="${PWD}/../NIST-SARD-Test-Suites"
  local vulnerableapp_local_repo="${PWD}/../VulnerableApp"
  local vulnerablejsapp_local_repo="${PWD}/../vulnerable_js_app"
  local cache_local=~/.skims/cache
  local cache_remote="s3://skims.data/cache/${CI_COMMIT_REF_NAME}"
  local skims_test_group="${1:-all}"

  echo '[INFO] Creating staging area' \
    && copy '__envAndroguardRepo__' "${androguard_local_repo}" \
    && copy '__envBenchmarkRepo__' "${benchmark_local_repo}" \
    && copy '__envNISTTestSuites__' "${nisttestsuites_local_repo}" \
    && copy '__envVulnerableAppRepo__' "${vulnerableapp_local_repo}" \
    && copy '__envVulnerableJsAppRepo__' "${vulnerablejsapp_local_repo}" \
    && aws_login_dev 'skims' \
    && aws_s3_sync "${cache_remote}" "${cache_local}" \
    && echo "[INFO] Running test suite with group: ${skims_test_group}" \
    && ensure_gitlab_env_var INTEGRATES_API_TOKEN \
    && pushd skims \
    && pytest \
      --capture tee-sys \
      --disable-pytest-warnings \
      --durations 10 \
      --exitfirst \
      --reruns 10 \
      --showlocals \
      --show-capture no \
      --skims-test-group "${skims_test_group}" \
      -vvv \
    && popd \
    && echo '[INFO] Cleaning environment' \
    && aws_s3_sync "${cache_local}" "${cache_remote}" \
    || return 1
}

main "${@}"
