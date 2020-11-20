# shellcheck shell=bash

function helper_sorts_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_DEFAULT_REGION='us-east-1'
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${SORTS_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SORTS_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${SORTS_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${SORTS_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_sorts_extract_features {
  local success

  export GITLAB_API_TOKEN
  export GITLAB_API_USER
  export INTEGRATES_API_TOKEN
  export SERVICES_PROD_AWS_ACCESS_KEY_ID
  export SERVICES_PROD_AWS_SECRET_ACCESS_KEY
  export SORTS_PROD_AWS_ACCESS_KEY_ID
  export SORTS_PROD_AWS_SECRET_ACCESS_KEY

      helper_common_use_services \
  &&  helper_sorts_aws_login prod \
  &&  echo '[INFO] Cloning repositories' \
  &&  { helper_common_pull_services_repositories "${group}" ||  true; } \
  &&  if ! test -e "groups/${group}/fusion"
      then
            echo '[WARNING] No repositories to test' \
        &&  return 0
      fi \
  &&  echo '[INFO] Running sorts:' \
  &&  if "${product}/bin/sorts" --get-file-data "groups/${group}"
      then
            echo "[INFO] Succesfully processed: ${group}" \
        &&  success='true'
      else
            echo "[ERROR] While running sorts on: ${group}" \
        &&  success='false'
      fi \
  &&  helper_sorts_push_csv_file_s3 "${group}" \
  &&  helper_common_remove_services_repositories "${group}" \
  &&  test "${success}" = 'true'
}

function helper_sorts_install_dependencies {
  export PYTHONPATH="${PWD}/sorts/.venv/lib64/python3.8/site-packages:${PYTHONPATH}"

  # If the lock does not exist
  if ! test -e sorts/poetry.lock
  then
          helper_common_poetry_install_deps sorts
  fi
}

function helper_sorts_push_csv_file_s3 {
  local group="${1}"
  local target="s3://sorts/features/"

      echo "[INFO] Uploading Sorts feature extraction result to S3" \
  &&  aws s3 sync --exclude "*" --include "${group}*.csv" --quiet . "${target}" \
  &&  rm -rf "./*.csv"
}

function helper_sorts_terraform_plan {
  local target="${1}"
  local config

      config="$(readlink -f ../.tflint.hcl)" \
  &&  helper_common_terraform_plan_new "${target}" "${config}"
}
