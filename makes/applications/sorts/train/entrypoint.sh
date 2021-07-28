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
    && python3.8 training/redshift/db.py init-db \
    && echo "[INFO] Initializing training..." \
    && python3.8 training/sagemaker_provisioner.py \
    && echo "[INFO] Evaluating resulting artifacts..." \
    && python3.8 training/evaluate_results.py train \
    && popd \
    || return 1
}

main "${@}"
