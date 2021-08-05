# shellcheck shell=bash

function populate {
  local email="${1:-integratesmanager@gmail.com}"
  local db_status="${2:-}"
  local db_design='__envNewDbDesign__/database-design.json'
  local TMP_ITEMS='.tmp_integrates_vms'
  local i=0

  if test "${db_status}" == 'migration'; then
    echo '[INFO] Populating from new database design...' \
      && jq -c '{integrates_vms: [{PutRequest: {Item: .DataModel[].TableFacets[].TableData[]}}]}' \
        ${db_design} > "${STATE_PATH}/${TMP_ITEMS}" \
      && items_len=$(jq '.integrates_vms | length' "${STATE_PATH}/${TMP_ITEMS}") \
      && echo "items qy: ${items_len}" \
      && while [ $((i * 25)) -lt "$items_len" ]; do
        local ilow=$((i * 25)) \
          && local ihigh=$(((i + 1) * 25)) \
          && jq -c "{integrates_vms: .integrates_vms[$ilow:$ihigh]}" \
            "${STATE_PATH}/${TMP_ITEMS}" > "${STATE_PATH}/integrates_vms${i}.json" \
          && ((i++))
      done \
      && rm "${STATE_PATH}/${TMP_ITEMS}"
  else
    echo "[INFO] Admin email: ${email}" \
      && sed "s/2020-09-04.*/$(date -u +%Y-%m-%dT%H:%M:%S.000000%z)\"/g" \
        < '__envDb__/data/forces.json' \
      | sed "s/33e5d863252940edbfb144ede56d56cf/aaa/g" \
        | sed "s/a125217504d447ada2b81da3e4bdab0e/bbb/g" \
          > "${STATE_PATH}/forces.now.json" \
      && for data in '__envDb__/data/'*'.json'; do
        sed "s/__adminEmail__/${email}/g" "${data}" \
          > "${STATE_PATH}/$(basename "${data}")"
      done
  fi \
    && for data in "${STATE_PATH}/"*'.json'; do
      echo "[INFO] Writing data from: ${data}" \
        && aws dynamodb batch-write-item \
          --endpoint-url "http://${HOST}:${PORT}" \
          --request-items "file://${data}" \
        || return 1
    done
}

function serve {
  echo '[INFO] Unpacking DynamoDB' \
    && rm -rf "${STATE_PATH}" \
    && mkdir -p "${STATE_PATH}" \
    && pushd "${STATE_PATH}" \
    && unzip -u '__envDynamoZip__' \
    && popd \
    && echo '[INFO] Deleting old instance, if exists' \
    && makes-kill-port "${PORT}" 28022 \
    && echo '[INFO] Launching DynamoDB' \
    && {
      java \
        -Djava.library.path="${STATE_PATH}/DynamoDBLocal_lib" \
        -jar "${STATE_PATH}/DynamoDBLocal.jar" \
        -inMemory \
        -port "${PORT}" \
        -sharedDb &
    } \
    && makes-wait 10 "${HOST}:${PORT}" \
    && copy __envDb__ "${STATE_PATH}/terraform" \
    && pushd "${STATE_PATH}/terraform" \
    && terraform init \
    && terraform apply -auto-approve \
    && popd \
    && if test "${POPULATE}" != 'false'; then
      populate "${@}"
    fi \
    && makes-done 28022 \
    && echo '[INFO] Dynamo DB is ready' \
    && wait
}

function serve_daemon {
  makes-kill-port 28022 \
    && { serve "${@}" & } \
    && makes-wait 60 localhost:28022
}

function main {
  export HOST="${HOST:-127.0.0.1}"
  export PORT="${PORT:-8022}"
  export DAEMON="${DAEMON:-false}"
  export POPULATE="${POPULATE:-true}"
  export TF_VAR_host="${HOST}"
  export TF_VAR_port="${PORT}"

  export AWS_ACCESS_KEY_ID='test'
  export AWS_SECRET_ACCESS_KEY='test'
  export AWS_DEFAULT_REGION='us-east-1'
  export STATE_PATH='.DB'

  case "${DAEMON:-}" in
    true) serve_daemon "${@}" ;;
    *) serve "${@}" ;;
  esac
}

main "${@}"
