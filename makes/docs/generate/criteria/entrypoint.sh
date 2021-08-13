# shellcheck shell=bash

function _copy {
  local origin="${1}"
  local destination="${2}"

  info "Copying ${origin} to ${destination}" \
    && copy "${origin}" "${destination}"
}

function _clean {
  local src="${1}"
  local regex="[0-9]{3}\.md"
  local targets=(
    "${src}/vulnerabilities"
    "${src}/requirements"
    "${src}/compliance"
  )

  for target in "${targets[@]}"; do
    info "Cleaning ${target}" \
      && find "${target}" -name "${regex}" -delete \
      || return 1
  done
}

function main {
  local src='docs/src/docs/criteria'
  local path_vulnerabilities="${src}/vulnerabilities"
  local path_requirements="${src}/requirements"
  local path_compliance="${src}/compliance"
  source __argVulnerabilities__/template vulnerabilities
  source __argRequirements__/template requirements
  source __argCompliance__/template compliance

  _clean "${src}" \
    && info Autogenerating Criteria \
    && for var in "${!vulnerabilities[@]}"; do
      _copy \
        "${vulnerabilities[${var}]}/template" \
        "${path_vulnerabilities}/${var}.md" \
        || return 1
    done \
    && for var in "${!requirements[@]}"; do
      _copy \
        "${requirements[${var}]}/template" \
        "${path_requirements}/${var}.md" \
        || return 1
    done \
    && for var in "${!compliance[@]}"; do
      _copy \
        "${compliance[${var}]}/template" \
        "${path_compliance}/${var}.md" \
        || return 1
    done
}

main "${@}"
