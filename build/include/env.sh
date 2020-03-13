# shellcheck shell=bash

source "${srcIncludeHelpers}"

function env_prepare_environment_variables {
  export IS_LOCAL_BUILD
  export ENVIRONMENT_NAME
  export STARTDIR="${PWD}"
  export WORKDIR="${PWD}.ephemeral"

      echo '[INFO] Sourcing .envrc.public' \
  &&  source './.envrc.public' \
  &&  if test -n "${CI:-}"
      then
            echo '[INFO] In remote build system' \
        && IS_LOCAL_BUILD="${FALSE}"
      else
            echo '[INFO] In local build system' \
        && IS_LOCAL_BUILD="${TRUE}"
      fi \
  &&  if test "${CI_COMMIT_REF_NAME}" = 'master'
      then
            echo '[INFO] In productive environment' \
        &&  ENVIRONMENT_NAME='prod'
      else
            echo '[INFO] In development environment' \
        &&  ENVIRONMENT_NAME='dev'
      fi
}
