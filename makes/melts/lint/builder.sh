# shellcheck shell=bash

source "${envSetupMeltsRuntime}"
source "${envBashLibLintPython}"

function main {
      target="${PWD}/toolbox" \
  &&  copy "${envSrcMelts}" "${target}" \
  &&  lint_python "${target}" \
  &&  success
}

main "${@}"
