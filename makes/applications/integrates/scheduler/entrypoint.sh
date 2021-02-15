# shellcheck shell=bash

function main {
  local module="backend.scheduler.${1}"

      echo "[INFO] Waking up: ${module}" \
  &&  pushd integrates \
    &&  aws_login_dev integrates \
    &&  sops_export_vars secrets-development.yaml "${INTEGRATES_SECRETS_LIST[@]}" \
    &&  python3 'back/packages/integrates-back/cli/invoker.py' "${module}" \
    &&  popd \
  ||  return 1
}

main "${@}"
