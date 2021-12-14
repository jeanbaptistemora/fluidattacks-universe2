# shellcheck shell=bash
alias timedoc-tokens="observes-service-timedoctor-tokens-bin"

function main {

  aws_login_prod_new 'observes' \
    && sops_export_vars 'observes/secrets-prod.yaml' \
      timedoctor_init_creds \
    && timedoc-tokens new-grant-code \
      --init-creds "${timedoctor_init_creds}"
}

main
