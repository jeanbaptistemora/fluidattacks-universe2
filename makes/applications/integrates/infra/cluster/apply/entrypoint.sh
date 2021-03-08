# shellcheck shell=bash

function main {
      aws_login_prod integrates \
  &&  aws_eks_update_kubeconfig 'integrates-cluster' 'us-east-1' \
  &&  sops_export_vars 'integrates/secrets-production.yaml' \
        CLOUDFLARE_API_TOKEN \
        NEW_RELIC_LICENSE_KEY \
  &&  TF_VAR_cloudflare_api_token="${CLOUDFLARE_API_TOKEN}" \
      TF_VAR_newrelic_license_key="${NEW_RELIC_LICENSE_KEY}" \
      terraforma-apply
}

main "${@}"
