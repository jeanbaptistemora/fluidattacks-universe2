# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
      aws_login_dev integrates \
  &&  sops_export_vars 'integrates/secrets-development.yaml' 'default' \
        CLOUDFLARE_API_TOKEN \
  &&  TF_VAR_cloudflare_api_token="${CLOUDFLARE_API_TOKEN}" \
      '__envTerraformTest__'
}

main "${@}"
