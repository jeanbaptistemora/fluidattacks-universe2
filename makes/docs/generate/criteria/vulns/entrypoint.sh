# shellcheck shell=bash

function main {
  local vulns_path="docs/src/docs/criteria2/vulnerabilities"
  source __argVulns__/template vulns

  info Autogenerating vulnerabilities \
    && info "Creating ${vulns_path}" \
    && mkdir -p "${vulns_path}" \
    && for var in "${!vulns[@]}"; do
      info "Copying ${vulns[${var}]}/template to ${vulns_path}/${var}.md" \
        && copy "${vulns[${var}]}/template" "${vulns_path}/${var}.md" \
        || return 1
    done
}

main "${@}"
