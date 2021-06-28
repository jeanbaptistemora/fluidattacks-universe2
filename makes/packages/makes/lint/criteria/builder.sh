# shellcheck shell=bash

function main {
  ajv compile -s "${envSrcVulnerabilitiesSchema}" \
    && ajv validate -s "${envSrcVulnerabilitiesSchema}" -d "${envSrcVulnerabilitiesSchemaData}" \
    && touch "${out}"
}

main "${@}"
