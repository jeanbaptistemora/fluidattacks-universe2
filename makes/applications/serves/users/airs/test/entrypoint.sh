# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
      aws_login_dev serves \
  &&  sops_export_vars 'serves/secrets/development.yaml' \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
  &&  TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
      TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}" \
      '__envTerraformTest__'
}

main "${@}"
