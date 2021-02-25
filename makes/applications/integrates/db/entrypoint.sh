# shellcheck shell=bash

function populate {
  local state_path="${1}"
  local host="${2}"
  local port="${3}"

      sed "s/2020-09-04.*/$(date -u +%Y-%m-%dT%H:%M:%S.000000%z)\"/g" \
        < '__envDb__/data/forces.json' \
        | sed "s/33e5d863252940edbfb144ede56d56cf/aaa/g" \
        | sed "s/a125217504d447ada2b81da3e4bdab0e/bbb/g" \
        > "${state_path}/forces.now.json" \
  &&  for data in '__envDb__/data/'*'.json' "${state_path}/"*'.json'
      do
            echo "[INFO] Writing data from: ${data}" \
        &&  aws dynamodb batch-write-item \
              --endpoint-url "http://${host}:${port}" \
              --request-items "file://${data}" \
        ||  return 1
      done
}

function serve {
  export AWS_ACCESS_KEY_ID='test'
  export AWS_SECRET_ACCESS_KEY='test'
  export AWS_DEFAULT_REGION='us-east-1'
  local host='127.0.0.1'
  local port='8022'
  local state_path='.DB'

      echo '[INFO] Unpacking DynamoDB' \
  &&  rm -rf "${state_path}" \
  &&  mkdir -p "${state_path}" \
  &&  pushd "${state_path}" \
    &&  unzip -u '__envDynamoZip__' \
  &&  popd \
  &&  echo '[INFO] Deleting old instance, if exists' \
  &&  makes-kill-port "${port}" 28022 \
  &&  echo '[INFO] Launching DynamoDB' \
  &&  { java \
          -Djava.library.path="${state_path}/DynamoDBLocal_lib" \
          -jar "${state_path}/DynamoDBLocal.jar" \
          -inMemory \
          -port "${port}" \
          -sharedDb \
      & } \
  &&  makes-wait 10 "${host}:${port}" \
  &&  copy __envDb__ "${state_path}/terraform" \
  &&  pushd "${state_path}/terraform" \
    &&  terraform init \
    &&  terraform apply -auto-approve \
  &&  popd \
  &&  if test "${POPULATE:-}" != 'false'
      then
        populate "${state_path}" "${host}" "${port}"
      fi \
  &&  makes-done 28022 \
  &&  echo '[INFO] Dynamo DB is ready' \
  &&  wait
}

function serve_daemon {
      makes-kill-port 28022 \
  &&  { serve "${@}" & } \
  &&  makes-wait 60 localhost:28022
}

function main {
  if test "${DAEMON:-}" = 'true'
  then
    serve_daemon "${@}"
  else
    serve "${@}"
  fi
}

main "${@}"
