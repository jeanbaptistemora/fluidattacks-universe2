# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcCiScriptsHelpersOthers}"

function env_prepare_environment_variables {
  export CI_JOB_NAME="${1}"
  export IS_NIX='true'
  export IS_LOCAL_BUILD
  export ENVIRONMENT_NAME
  export FI_VERSION
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
        &&  ENVIRONMENT_NAME="production"
      else
            echo '[INFO] In development environment' \
        &&  ENVIRONMENT_NAME="development"
      fi \
  &&  FI_VERSION=$(app_version) \
  &&  FI_VERSION_MOBILE=$(mobile_get_version code) \
  &&  echo "[INFO] FI_VERSION: ${FI_VERSION}" \
  &&  echo "[INFO] FI_VERSION_MOBILE: ${FI_VERSION_MOBILE}"
}

function env_prepare_ephemeral_vars {
  export MYPY_CACHE_DIR
  export TEMP_FD
  export TEMP_FILE1
  export TEMP_FILE2

  MYPY_CACHE_DIR=$(mktemp)
  exec {TEMP_FD}>TEMP_FD
  TEMP_FILE1=$(mktemp)
  TEMP_FILE2=$(mktemp)
}

function env_prepare_python_packages {
  export PATH
  export PYTHONPATH
  local pkg

  echo '[INFO] Preparing python packages'

  helper_list_vars_with_regex 'pyPkg[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r pkg
  do
    echo "  [${pkg}] ${!pkg}"
    PATH="${PATH}:${!pkg}/site-packages/bin"
    PYTHONPATH="${PYTHONPATH}:${!pkg}/site-packages"
  done < "${TEMP_FILE1}"
}

function env_prepare_python_async_packages {
  export PATH
  export PYTHONPATH
  local pkg

  echo '[INFO] Preparing extra python packages'

  helper_list_vars_with_regex 'pyAsyncPkg[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r pkg
  do
    echo "  [${pkg}] ${!pkg}"
    PATH="${PATH}:${!pkg}/site-packages/bin"
    PYTHONPATH="${!pkg}/site-packages:${PYTHONPATH}"
  done < "${TEMP_FILE1}"

  # Override Graphene-django's graphql-core with Ariadne's graphql-core
  PYTHONPATH="${pyAsyncPkgReqs}/site-packages:${PYTHONPATH}"

  chmod --recursive u+w "${pyAsyncPkgIntegratesBack}"

  for cursrc in dal decorators.py domain exceptions.py mailer.py \
        scheduler.py services.py util.py utils; do
    echo "  [MIGRATION] Copying ${cursrc}..."
    cp -a "${pyPkgIntegratesBack}"/site-packages/backend/${cursrc} \
        "${pyAsyncPkgIntegratesBack}"/site-packages/backend/
    done
}

function env_prepare_nodejs_modules {
  export NODE_PATH
  local module

  echo '[INFO] Preparing Node.js modules'

  helper_list_vars_with_regex 'nodejsModule[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r module
  do
    echo "  [${module}] ${!module}"
    NODE_PATH="${NODE_PATH}:${!module}/node_modules"
  done < "${TEMP_FILE1}"
}

function env_prepare_ruby_modules {
  export PATH
  export GEM_PATH
  local gem

  echo '[INFO] Preparing ruby gems'

  helper_list_vars_with_regex 'rubyGem[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r gem
  do
    echo "  [${gem}] ${!gem}"
    PATH="${PATH}:${!gem}/bin"
    GEM_PATH="${GEM_PATH}:${!gem}/"
  done < "${TEMP_FILE1}"
}

function env_prepare_dynamodb_local {
      echo '[INFO] Unzipping DynamoDB local' \
  &&  mkdir -p './.DynamoDB' \
  &&  pushd './.DynamoDB' \
    &&  unzip -u "${srcExternalDynamoDbLocal}" \
  && popd \
  ||  return 1
}
