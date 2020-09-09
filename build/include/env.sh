# shellcheck shell=bash

source "${srcIncludeHelpersCommon}"
source "${srcIncludeHelpersIntegrates}"

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
  &&  if test -n "${srcProduct:-}"
      then
        export PATH="${srcProduct}/bin:${PATH:-}"
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

function env_prepare_node_modules {
  export PATH
  export NODE_PATH
  local module

  echo '[INFO] Preparing node modules'

  helper_list_vars_with_regex 'nodeJsModule[a-zA-Z0-9]+' > "${TEMP_FILE1}"

  while read -r module
  do
    echo "  [${module}] ${!module}"
    PATH="${PATH}:${!module}/node_modules/.bin"
    NODE_PATH="${NODE_PATH}:${!module}/node_modules"
  done < "${TEMP_FILE1}"
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

function env_prepare_minio_local {
  export PYTHONPATH
  export FI_MINIO_LOCAL_ENABLED
  # MinIO credentials are only for local test development enviroment
  export MINIO_ACCESS_KEY="test_access_key"
  export MINIO_SECRET_KEY="test_secret_key"
  export MINIO_REGION_NAME
  export USER_MINIO_ACCESS_KEY
  export USER_MINIO_SECRET_KEY
  export minio
  export mc
      echo '[INFO] Preparing MinIO local' \
  &&  mkdir -p './.MinIO' \
  &&  env_prepare_python_packages \
  &&  PYTHONPATH="${PYTHONPATH}:${STARTDIR}/integrates" \
  &&  FI_MINIO_LOCAL_ENABLED='True' \
  &&  helper_integrates_set_dev_secrets \
  &&  MINIO_REGION_NAME="${AWS_DEFAULT_REGION}" \
  &&  USER_MINIO_ACCESS_KEY="${AWS_ACCESS_KEY_ID}" \
  &&  USER_MINIO_SECRET_KEY="${AWS_SECRET_ACCESS_KEY}" \
  &&  minio="${srcExternalMinIOLocal}" \
  &&  mc="${srcExternalMinIOCli}" \
  &&  chmod +x "${minio}" \
  &&  chmod +x "${mc}" \
  &&  pushd './.MinIO' \
    &&  mkdir -p './temp' \
    &&  mkdir -p './data' \
  && popd \
  ||  return 1
}

function env_prepare_django_static_external {
      echo '[INFO] Unzipping C3 local' \
  &&  mkdir -p 'app/static/external/C3' \
  &&  pushd 'app/static/external/C3' \
    &&  unzip -ou "${srcExternalC3}" \
  && popd \
  ||  return 1
}
