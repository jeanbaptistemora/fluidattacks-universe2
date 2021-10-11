# shellcheck shell=bash

function main {
  export SORTS_PROD_AWS_ACCESS_KEY_ID
  export SORTS_PROD_AWS_SECRET_ACCESS_KEY

  aws_login_prod 'sorts' \
    && sops_export_vars 'sorts/secrets.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && pushd sorts \
    && echo "[INFO] Preparing extracted features data..." \
    && python3.8 training/merge_features.py \
    && popd \
    || return 1

}

main "${@}"
