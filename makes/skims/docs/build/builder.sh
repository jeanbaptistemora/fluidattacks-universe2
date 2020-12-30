# shellcheck shell=bash

source "${makeDerivation}"
source "${envSetupSkimsDevelopment}"
source "${envSetupSkimsRuntime}"

function main {
      echo '[INFO] Creating a staging area' \
  &&  copy "${envSrcSkimsDocs}" "${PWD}/docs" \
  &&  copy "${envSrcSkimsSkims}" "${PWD}/skims" \
  &&  copy "${envSrcSkimsReadme}" "${PWD}/README.md" \
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
