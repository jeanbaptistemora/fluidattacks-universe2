#!/usr/bin/env bash

# This file can be imported from anywhere by running:
# . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)

create_sops_file() {
  export SOPS_KMS_ARN
  local file
  local key_alias
  local profile

  # Create encrypted file with sops using one aws kms key
  # e.g: create_sops_file vars-production.yaml alias/serves-production serves-admin

      file="${1}" \
  &&  key_alias="${2}" \
  &&  profile="${3}" \
  &&  SOPS_KMS_ARN=$( \
        aws --profile "${profile}" kms describe-key --key-id "${key_alias}" \
          | jq -r .KeyMetadata.Arn ) \
  &&  sops --aws-profile "${profile}" "${file}"
}

sops_env() {
  local file
  local decrypted_json
  local profile
  local variable_name

  # Export variables from sops yaml file
  # e.g: sops_env secrets-production.yaml serves-admin var1 var2 var3 var4
  # note: needs jq

      file="${1}" \
  &&  profile="${2}" \
  &&  decrypted_json=$( \
        sops \
          --aws-profile "${profile}" \
          --decrypt \
          --output-type json \
          "${file}") \
  &&  shift 2 \
  &&  for variable_name in "${@}"; do
            echo "Exporting: ${variable_name}" \
        &&  variable_value=$( \
              echo "${decrypted_json}" \
                | jq -r ".${variable_name}") \
        &&  export "${variable_name//./__}=${variable_value}"
      done
}
