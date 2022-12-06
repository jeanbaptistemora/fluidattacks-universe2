# shellcheck shell=bash

function _get_keys {
  aws ec2 describe-key-pairs | jq -rec ".[][].KeyName" | grep -E "^runner"
}

function _delete_key {
  local key="${1}"

  : \
    && info "Deleting key: ${key}" \
    && aws ec2 delete-key-pair --key-name "${key}"
}

function main {
  local keys

  : \
    && keys=$(_get_keys) \
    && while read -r key; do
      _delete_key "${key}"
    done <<< "${keys}"
}

main "${@}"
