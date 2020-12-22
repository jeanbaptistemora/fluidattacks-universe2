# shellcheck shell=bash

source "${makeDerivation}"
source "${envBashLibPython}"

function main {
      make_python_path \
        "${envPythonRequirementsDevelopment}" \
        "${envPythonRequirementsRuntime}" \
        "${envSrcSkimsSkims}" \
  &&  success
}

main "${@}"
