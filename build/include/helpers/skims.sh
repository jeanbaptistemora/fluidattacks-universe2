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

function helper_skims_compile_parsers {
  export CLASSPATH
  export srcExternalANTLR4
  local compile_antlr=(java -jar "${srcExternalANTLR4}" -no-listener -no-visitor)
  local compile_java=(javac -Werror)

      echo '[INFO] Compiling grammars' \
  &&  pushd skims/static/parsers/ \
    &&  export CLASSPATH=".:${srcExternalANTLR4}:${CLASSPATH:-}" \
    &&  echo "[INFO] Building ANTLR parsers" \
    &&  pushd antlr \
      &&  for name in CSharp Java9 Scala
          do
                echo "[INFO] Building ANTLR-${name} parser" \
            &&  "${compile_antlr[@]}" "src/main/java/parse/${name}"*".g4" \
            &&  "${compile_java[@]}" "src/main/java/parse/${name}"*".java" \
            ||  return 1
          done \
      &&  gradle installDist \
    &&  popd \
    &&  echo "[INFO] Building Babel parsers" \
    &&  pushd babel \
      &&  npm install \
    &&  popd \
  &&  popd \
  ||  return 1
}

function helper_skims_compute_dependencies_cache_key {
  export CI_COMMIT_REF_NAME
  export IS_LOCAL_BUILD

  echo "branch:${CI_COMMIT_REF_NAME}-local:${IS_LOCAL_BUILD}"
}

function helper_skims_install_dependencies {
  export PYTHONPATH="${PWD}/skims/.venv/lib64/python3.8/site-packages"

      env_prepare_nix_overriden_python_packages \
  &&  helper_skims_install_poetry_dependencies
}

function helper_skims_install_poetry_dependencies {
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

function helper_skims_terraform_plan {
  local target="${1}"
  local config

      config="$(readlink -f ../.tflint.hcl)" \
  &&  helper_common_terraform_plan_new "${target}" "${config}"
}
