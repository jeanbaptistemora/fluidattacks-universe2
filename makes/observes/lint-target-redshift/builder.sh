# shellcheck shell=bash

source "${envBashLibLintPython}"
source "${envSetupObservesTargetRedshift}"
function main {
      lint_python "${envSrcObservesTargetRedshift}" \
  &&  success

}

main "${@}"
