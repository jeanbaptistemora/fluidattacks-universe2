# shellcheck shell=bash

function main {
  local group_id="235242"
  local result

  aws_login_dev \
    && sops_export_vars "__argCommonStatusSecrets__" \
      COMMAND_LINE_TRIGGER \
    && result="$(curl "https://api.checklyhq.com/check-groups/${group_id}/trigger/${COMMAND_LINE_TRIGGER}")" \
    && info "Check results:" \
    && echo "${result}" | jq . \
    && test "$(echo "${result}" | grep -c '"hasFailures":true')" -eq 0
}

main "${@}"
