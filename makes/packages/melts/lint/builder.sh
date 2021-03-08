# shellcheck shell=bash

source "${envSetupMeltsRuntime}"
source "${envSetupMeltsDevelopment}"

function main {
      lint_python_module "${envSrcMeltsToolbox}" \
  &&  lint_python_module "${envSrcMeltsTest}" \
  &&  touch "${out}"
}

main "${@}"
