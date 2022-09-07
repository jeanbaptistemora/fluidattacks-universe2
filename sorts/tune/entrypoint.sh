# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  export AWS_DEFAULT_REGION="us-east-1"

  : \
    && aws_login "prod_sorts" "3600" \
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
