# shellcheck shell=bash
alias timedoc-tokens="observes-service-timedoctor-tokens-bin"

function main {

  : \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      timedoctor_init_creds \
      bugsnag_notifier_key \
    && timedoc-tokens new-grant-code \
      --init-creds "${timedoctor_init_creds}"
}

main
