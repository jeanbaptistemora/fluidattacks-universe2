# shellcheck shell=bash

source "${envSetupMeltsRuntime}"
source "${envSetupMeltsDevelopment}"
source "${envBashLibLintPython}"

function main {
      lint_python_module "${envSrcMeltsToolbox}" \
  &&  lint_python_module "${envSrcMeltsTest}" \
  &&  success
}

main "${@}"
