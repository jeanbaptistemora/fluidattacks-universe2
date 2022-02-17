# shellcheck shell=bash

function main {
  aws_login_prod_new 'sorts' \
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
