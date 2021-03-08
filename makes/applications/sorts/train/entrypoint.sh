# shellcheck shell=bash

function main {
  export SORTS_PROD_AWS_ACCESS_KEY_ID
  export SORTS_PROD_AWS_SECRET_ACCESS_KEY

      aws_login_prod 'sorts' \
  &&  pushd sorts \
    &&  echo "[INFO] Preparing extracted features data..." \
    &&  python3.8 training/merge_features.py \
    &&  echo "[INFO] Initializing training..." \
    &&  python3.8 training/sagemaker_provisioner.py \
    &&  echo "[INFO] Evaluating resulting artifacts..." \
    &&  python3.8 training/evaluate_results.py \
  &&  popd \
  || return 1
}

main "${@}"
