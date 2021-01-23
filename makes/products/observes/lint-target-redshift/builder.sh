# shellcheck shell=bash

source "${envBashLibLintPython}"
source "${envSetupObservesTargetRedshift}"

function main {
      lint_python_module "${envSrcObservesTargetRedshift}" \
  &&  success
}

main "${@}"
