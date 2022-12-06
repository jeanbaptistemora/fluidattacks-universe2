# shellcheck shell=bash

function _get_keys {
  aws ec2 describe-key-pairs | jq -rec ".[][].KeyName" | grep -E "^runner"
}

function _get_used_keys {
  aws ec2 describe-instances | jq -rec ".[][].Instances[].KeyName" | uniq
}

function _delete_key {
  local key="${1}"

  : \
    && info "Deleting key: ${key}" \
    && aws ec2 delete-key-pair --key-name "${key}"
}

function main {
  local keys
  local used_keys

  : \
    && keys=$(_get_keys) \
    && used_keys=$(_get_used_keys) \
    && while read -r key; do
      if ! grep -q "${key}" <<< "${used_keys}"; then
        _delete_key "${key}"
      else
        info "Key is being currently used: ${key}"
      fi
    done <<< "${keys}"
}

main "${@}"
