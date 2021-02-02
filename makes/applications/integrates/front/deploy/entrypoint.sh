# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsCommon__'

function main {
  export CI_COMMIT_REF_NAME
  local env='development'

      if [ "${CI_COMMIT_REF_NAME}" == "master" ]
      then
            env='production' \
        &&  aws_login_prod integrates
      else
        aws_login_dev integrates
      fi \
  &&  pushd integrates \
    &&  mkdir -p app/static/external/C3 \
    &&  copy '__envExternalC3__' app/static/external/C3 \
    &&  copy back/app/templates/static app/static \
    &&  aws_s3_sync \
          app \
          "s3://integrates.front.${env}.fluidattacks.com/${CI_COMMIT_REF_NAME}/" \
          --delete \
  &&  popd \
  ||  return 1
}

main "${@}"
