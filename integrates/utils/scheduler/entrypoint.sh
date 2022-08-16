# shellcheck shell=bash

function main {
  local env="${1:-}"
  local module="${2:-}"
  export SKIMS_FLUID_WATERMARK='__argSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png'
  export SKIMS_ROBOTO_FONT='__argSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf'

  echo "[INFO] Waking up: ${module}" \
    && source __argIntegratesBackEnv__/template "${env}" \
    && if test -z "${module:-}"; then
      echo '[ERROR] Second argument must be the module to execute' \
        && return 1
    fi \
    && pushd integrates \
    && python3 'back/src/cli/invoker.py' "${module}" \
    && popd \
    || return 1
}

main "${@}"
