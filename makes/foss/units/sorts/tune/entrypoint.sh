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
    && echo "[INFO] Tuning best model hyperparamters..." \
    && python3.8 training/tune_hyperparameters.py \
    && echo "[INFO] Evaluating resulting artifacts..." \
    && python3.8 training/evaluate_results.py tune \
    && popd \
    || return 1
}

main "${@}"
