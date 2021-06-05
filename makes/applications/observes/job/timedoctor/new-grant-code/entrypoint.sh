# shellcheck shell=bash
alias timedoc-tokens="observes-bin-service-timedoctor-tokens"

function main {

  aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      timedoctor_init_creds \
    && timedoc-tokens new-grant-code \
      --init-creds "${timedoctor_init_creds}"
}

main
