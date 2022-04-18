# shellcheck shell=bash
alias timedoc-tokens="observes-service-timedoctor-tokens-bin"

function main {

  aws_login_prod 'observes' \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      timedoctor_init_creds \
    && timedoc-tokens set-init-token \
      --init-creds "${timedoctor_init_creds}"
}

main
