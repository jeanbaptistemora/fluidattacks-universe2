# shellcheck shell=bash

function main {
      aws_login_prod makes \
  &&  sops_export_vars 'makes/applications/makes/secrets/src/production.yaml' \
        CI_REGISTRATION_TOKEN \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
        NEW_RELIC_LICENSE_KEY \
  &&  TF_VAR_ci_cache_access_key="${MAKES_PROD_AWS_ACCESS_KEY_ID}" \
      TF_VAR_ci_cache_secret_key="${MAKES_PROD_AWS_SECRET_ACCESS_KEY}" \
      TF_VAR_ci_registration_token="${CI_REGISTRATION_TOKEN}" \
      TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
      TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}" \
      TF_VAR_newrelic_license_key="${NEW_RELIC_LICENSE_KEY}" \
      terraform-apply
}

main "${@}"
