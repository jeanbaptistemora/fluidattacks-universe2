# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
      aws_login_prod serves \
  &&  sops_export_vars 'serves/secret-management/development.yaml' \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
  &&  TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
      TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}" \
      '__envTerraformApply__'
}

main "${@}"
