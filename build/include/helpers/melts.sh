# shellcheck shell=bash

function helper_test_lint_code_python {
  local args_mypy=(
    --allow-any-generics
    # Remove following rule when all packages in melts are typed
    --follow-imports=skip
    --ignore-missing-imports
  )

      pushd melts \
  &&  echo '[INFO]: Checking static typing...' \
  &&  mypy "${args_mypy[@]}" . \
  &&  echo '[INFO]: Linting...' \
  &&  prospector --profile prospector_config.yml . \
  &&  popd \
  || return 1
}

function helper_clone_test_repo {
  export GITLAB_API_TOKEN

      git clone \
  "https://gitlab.com:${GITLAB_API_TOKEN}@gitlab.com/fluidattacks/services.git" \
  &&  pushd services \
  &&  git checkout HEAD groups/continuoustest/ \
  &&  popd || exit
}

function helper_melts_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${MELTS_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${MELTS_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${MELTS_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${MELTS_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}