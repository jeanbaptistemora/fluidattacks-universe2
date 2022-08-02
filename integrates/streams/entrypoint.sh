# shellcheck shell=bash
function main {
  local module="${1:-}"
  local secrets=(
    AWS_OPENSEARCH_HOST
  )

  echo "[INFO] Executing ${module} consumer" \
    && sops_export_vars __argSecretsProd__ "${secrets[@]}" \
    && pushd integrates/streams/src \
    && python3 "invoker.py" "${module}" \
    && popd \
    || return 1
}

main "${@}"
