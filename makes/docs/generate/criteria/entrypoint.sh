# shellcheck shell=bash

function _create_path {
  local target="${1}"

  info "Creating ${target}" \
    && mkdir -p "${target}"
}

function _copy {
  local origin="${1}"
  local destination="${2}"

  info "Copying ${origin} to ${destination}" \
    && copy "${origin}" "${destination}"
}

function main {
  declare -A paths=(
    [vulnerabilities]="docs/src/docs/criteria2/vulnerabilities"
    [requirements]="docs/src/docs/criteria2/requirements"
    [compliance]="docs/src/docs/criteria2/compliance"
  )
  source __argVulnerabilities__/template vulnerabilities
  source __argRequirements__/template requirements
  source __argCompliance__/template compliance

  info Autogenerating Criteria \
    && for path in "${paths[@]}"; do
      _create_path "${path}" \
        || return 1
    done \
    && for var in "${!vulnerabilities[@]}"; do
      _copy \
        "${vulnerabilities[${var}]}/template" \
        "${paths[vulnerabilities]}/${var}.md" \
        || return 1
    done \
    && for var in "${!requirements[@]}"; do
      _copy \
        "${requirements[${var}]}/template" \
        "${paths[requirements]}/${var}.md" \
        || return 1
    done \
    && for var in "${!compliance[@]}"; do
      _copy \
        "${compliance[${var}]}/template" \
        "${paths[compliance]}/${var}.md" \
        || return 1
    done
}

main "${@}"
