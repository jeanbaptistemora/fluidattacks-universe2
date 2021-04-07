# shellcheck shell=bash

function main {
      aws_login_dev makes \
  &&  sops_export_vars 'makes/applications/makes/secrets/src/development.yaml' \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
  &&  TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
      TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}" \
      terraform-test
}

main "${@}"
