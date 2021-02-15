# shellcheck shell=bash

function main {
  local env="${1:-}"
  local module="${2:-}"

      echo "[INFO] Waking up: ${module}" \
  &&  source __envIntegratesEnv__ "${env}" \
  &&  if test -z "${module:-}"
      then
            echo '[ERROR] Second argument must be the module to execute' \
        &&  return 1
      fi \
  &&  pushd integrates \
    &&  python3 'back/packages/integrates-back/cli/invoker.py' "${module}" \
  &&  popd \
  ||  return 1
}

main "${@}"
