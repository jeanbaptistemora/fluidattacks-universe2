# shellcheck shell=bash

function main {
  export TF_VAR_okta_api_token
  export TF_VAR_okta_data

      "aws_login___envPermissions__" "__envProduct__" \
  &&  sops_export_vars "__envData__" \
        OKTA_API_TOKEN \
        OKTA_DATA_RAW \
  &&  TF_VAR_okta_api_token="${OKTA_API_TOKEN}" \
  &&  echo '[INFO] Parsing: OKTA_DATA_RAW' \
  &&  TF_VAR_okta_data="$(python3 "__envParser__")" \
  &&  terraform
}

main "${@}"
