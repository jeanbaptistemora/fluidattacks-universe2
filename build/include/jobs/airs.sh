# shellcheck shell=bash

function job_airs_deploy_local {
      helper_common_use_pristine_workdir \
  &&  airs dev \
  ||  return 1
}

function job_airs_deploy_ephemeral {
      helper_common_use_pristine_workdir \
  &&  airs eph \
  ||  return 1
}

function job_airs_deploy_production {
      helper_common_use_pristine_workdir \
  &&  airs prod \
  ||  return 1
}
