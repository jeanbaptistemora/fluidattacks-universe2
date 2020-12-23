# shellcheck shell=bash

source "${makeDerivation}"
source "${envBashLibPython}"
source "${envContextFile}"

function main {
      echo '[INFO] Creating a staging area' \
  &&  copy "${envSrcSkimsDocs}" "${PWD}/docs" \
  &&  copy "${envSrcSkimsSkims}" "${PWD}/skims" \
  &&  copy "${envSrcSkimsReadme}" "${PWD}/README.md" \
  &&  make_python_path '3.8' \
        "${envPythonRequirementsDevelopment}" \
        "${envPythonRequirementsRuntime}" \
  &&  make_python_path_plain \
        "${envSrcSkimsSkims}" \
        "${PWD}" \
  &&  echo '[INFO] Building docs' \
  &&  HOME=.
      pdoc \
        --force \
        --html \
        --output-dir "${PWD}" \
        --template-dir "${PWD}/docs/templates" \
        skims \
  &&  mv "${PWD}/skims" "${out}"
}

main "${@}"
