# shellcheck shell=bash

function main {
      aws_login_dev makes \
  &&  aws_eks_update_kubeconfig 'integrates-cluster' 'us-east-1' \
  &&  sops_export_vars 'makes/applications/makes/secrets/src/development.yaml' \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
        NEW_RELIC_LICENSE_KEY \
  &&  TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
      TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}" \
      TF_VAR_newrelic_license_key="${NEW_RELIC_LICENSE_KEY}" \
      terraform-test
}

main "${@}"
