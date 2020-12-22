# shellcheck shell=bash

source "${makeDerivation}"
source "${envBashLibPython}"

function main {
      make_python_path \
        "${envPythonRequirementsDevelopment}" \
        "${envPythonRequirementsRuntime}" \
        "${envSrcSkimsSkims}" \
  &&  echo '[INFO] Running bandig' \
  &&  bandit --recursive "${envSrcSkimsSkims}" \
  &&  success
}

main "${@}"
