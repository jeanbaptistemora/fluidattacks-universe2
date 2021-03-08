# shellcheck shell=bash

function deploy {
  local env="${1}"
  local endpoint="${2}"
  local branch="${3}"
  local front_path="${4}"

      "aws_login_${env}" integrates \
  &&  pushd integrates \
    &&  mkdir -p app/static \
    &&  copy "${front_path}/output/app/static" app/static \
    &&  aws_s3_sync \
          app \
          "s3://integrates.front.${endpoint}.fluidattacks.com/${branch}/" \
          --delete \
  &&  popd \
  ||  return 1
}
