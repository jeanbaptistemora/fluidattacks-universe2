# shellcheck shell=bash

source '__envSetupSortsDevelopment__'
source '__envUtilsBashLibAws__'

function main {
  export SORTS_PROD_AWS_ACCESS_KEY_ID
  export SORTS_PROD_AWS_SECRET_ACCESS_KEY

      aws_login_prod 'sorts' \
  &&  pushd sorts \
    &&  echo "[INFO] Preparing extracted features data..." \
    &&  '__envPython__' training/merge_features.py \
    &&  echo "[INFO] Initializing training..." \
    &&  '__envPython__' training/sagemaker_provisioner.py \
  &&  popd \
  || return 1
}

main "${@}"
