# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcExternalSops}"
source "${srcCiScriptsHelpersSops}"

function job_serve_dynamodb_local {
  local port=8022

      echo '[INFO] Launching DynamoDB local' \
  &&  {
        java \
          -Djava.library.path=./.DynamoDB/DynamoDBLocal_lib \
          -jar ./.DynamoDB/DynamoDBLocal.jar \
          -inMemory \
          -port "${port}" \
          -sharedDb \
        &
      } \
  &&  echo '[INFO] Waiting 5 seconds to leave DynamoDB start' \
  &&  sleep 5 \
  &&  echo '[INFO] Populating DynamoDB local' \
  &&  bash ./deploy/containers/common/vars/provision_local_db.sh \
  &&  echo "[INFO] DynamoDB is ready and listening on port ${port}!" \
  &&  echo "[INFO] Hit Ctrl+C to exit" \
  &&  fg %1
}

function job_serve_front {
      pushd front \
    &&  npm start \
  &&  popd
}

function job_serve_redis {
  local port=6379

      echo "[INFO] Serving redis on port ${port}" \
  &&  redis-server --port "${port}"
}

function job_serve_back_dev {
  export JWT_TOKEN
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export AWS_DEFAULT_REGION
  local app='fluidintegrates.asgi:application'
  local host='0.0.0.0'
  local port='8080'
  local root_path='/integrates'
  local workers='4'

      JWT_TOKEN=$(helper_get_gitlab_var JWT_TOKEN) \
  &&  AWS_ACCESS_KEY_ID=$(helper_get_gitlab_var DEV_AWS_ACCESS_KEY_ID) \
  &&  AWS_SECRET_ACCESS_KEY=$(helper_get_gitlab_var DEV_AWS_SECRET_ACCESS_KEY) \
  &&  AWS_DEFAULT_REGION='us-east-1' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1' \
  &&  echo '[INFO] Exporting development secrets' \
  &&  sops_vars development \
  &&  echo "[INFO] Serving back on port ${port}" \
  &&  uvicorn \
        --host="${host}" \
        --port="${port}" \
        --root-path="${root_path}" \
        --ssl-certfile="${srcDerivationsCerts}/fluidla.crt" \
        --ssl-keyfile="${srcDerivationsCerts}/fluidla.key" \
        --workers="${workers}" \
        "${app}"
}
