# shellcheck shell=bash

source "${envSetupForcesRuntime}"
source "${envSetupForcesDevelopment}"
source "${envBashLibLintPython}"

function main {
      lint_python_module "${envSrcForcesForces}" \
  &&  lint_python_module "${envSrcForcesTest}" \
  &&  success
}

main "${@}"
