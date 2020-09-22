# shellcheck shell=bash

function helper_skims_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${SKIMS_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SKIMS_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${SKIMS_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SKIMS_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_skims_compute_version {
  poetry run python -c 'if True:
    import time
    now=time.gmtime()
    minutes_month=(
      (now.tm_mday - 1) * 1440
      + now.tm_hour * 60
      + now.tm_min
    )
    print(time.strftime(f"%y.%m.{minutes_month}"))
  '
}

function helper_skims_compile_ast {
  export CLASSPATH
  export srcExternalANTLR4
  local grammars=(
    Java9
  )

      echo '[INFO] Compiling grammars' \
  &&  pushd skims/static/ast/ \
    &&  export CLASSPATH=".:${srcExternalANTLR4}:${CLASSPATH:-}" \
    &&  for grammar in "${grammars[@]}"
        do
              echo "[INFO] Processing: ${grammar}" \
          &&  java -jar "${srcExternalANTLR4}" src/main/java/ast/Java9.g4 \
          &&  echo "[INFO] Compiling: ${grammar}" \
          &&  javac -Werror src/main/java/ast/Java9*.java \

        done \
    &&  echo '[INFO] Building AST tool' \
    &&  gradle installDist \
  &&  popd \
  ||  return 1
}

function helper_skims_compute_dependencies_cache_key {
  export CI_COMMIT_REF_NAME
  export IS_LOCAL_BUILD

  echo "branch:${CI_COMMIT_REF_NAME}-local:${IS_LOCAL_BUILD}"
}

function helper_skims_install_dependencies {
  export PYTHONPATH="${PWD}/skims/.venv/lib64/python3.8/site-packages:${PYTHONPATH}"

  # If the lock does not exist
  if ! test -e skims/poetry.lock
  then
    # Attempt to unpack them from S3
    if ! helper_skims_dependencies_unpack
    then
      # If we could not do that, then install and pack them to S3
          helper_common_poetry_install_deps skims \
      &&  helper_skims_dependencies_pack
    fi
  fi
}

function helper_skims_dependencies_pack {
  local cache_key

      echo '[INFO] Packing dependencies' \
  &&  cache_key=$(helper_skims_compute_dependencies_cache_key) \
  &&  helper_skims_aws_login dev \
  &&  tar -czf "${TEMP_FILE1}" \
        skims/.venv/ \
        skims/poetry.lock \
  &&  aws s3 cp "${TEMP_FILE1}" "s3://skims.data/dependencies/${cache_key}/bundle.tar.gz"
}

function helper_skims_dependencies_unpack {
  local cache_key

      echo '[INFO] Unpacking dependencies' \
  &&  cache_key=$(helper_skims_compute_dependencies_cache_key) \
  &&  helper_skims_aws_login dev \
  &&  aws s3 cp "s3://skims.data/dependencies/${cache_key}/bundle.tar.gz" "${TEMP_FILE1}" \
  &&  tar --no-same-owner -xf "${TEMP_FILE1}"
}
