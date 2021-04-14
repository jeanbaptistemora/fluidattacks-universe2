# shellcheck shell=bash

function main {
  local cluster_name='makes-k8s'

      aws_login_prod makes \
  &&  if aws eks list-clusters | grep -q "${cluster_name}"
      then
        aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1'
      fi \
  &&  sops_export_vars 'makes/applications/makes/secrets/src/production.yaml' \
        CLOUDFLARE_EMAIL \
        CLOUDFLARE_API_KEY \
        NEW_RELIC_LICENSE_KEY \
  &&  TF_VAR_cloudflare_email="${CLOUDFLARE_EMAIL}" \
      TF_VAR_cloudflare_api_key="${CLOUDFLARE_API_KEY}" \
      TF_VAR_newrelic_license_key="${NEW_RELIC_LICENSE_KEY}" \
      terraform-apply
}

main "${@}"
