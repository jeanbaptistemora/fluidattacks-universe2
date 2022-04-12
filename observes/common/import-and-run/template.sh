# shellcheck shell=bash

function import_and_run {
  local module="${1}"
  local function="${2}"

  python -c "from ${module} import ${function}; ${function}()" "${@:3}"
}
