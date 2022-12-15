# shellcheck shell=bash

function execute_analytics_generator {
  local generator="${1}"
  local results_dir="${generator//.py/}"

  mkdir -p "${results_dir}" \
    && echo "[INFO] Running: ${generator}" \
    && {
      RESULTS_DIR="${results_dir}" python3 "${generator}" \
        || RESULTS_DIR="${results_dir}" python3 "${generator}" \
        || RESULTS_DIR="${results_dir}" python3 "${generator}"
    }
}

function main {
  local env="${1}"
  local parallel="${2}"
  local runtime="${3}"
  local todo

  source __argIntegratesBackEnv__/template "${env}" \
    && if test "${env}" = "dev"; then
      : \
        && DAEMON=true integrates-db \
        && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}-charts-documents/" \
        && populate_storage "/${CI_COMMIT_REF_NAME}-charts-documents"
    elif test "${env}" = "prod"; then
      :
    else
      error "Only 'dev' and 'prod' allowed for env."
    fi \
    && pushd integrates \
    && todo=$(mktemp) \
    && find "charts/generators" ! -name '__init__.py' ! -name 'utils*.py' ! -name 'common.py' ! -name 'colors.py' -wholename "*.py" | sort > "${todo}" \
    && execute_chunk_parallel execute_analytics_generator "${todo}" "${parallel}" "${runtime}" \
    && aws_s3_sync \
      "charts/generators" \
      "s3://integrates/analytics/${CI_COMMIT_REF_NAME}/documents" \
    && popd \
    || return 1
}

main "${@}"
