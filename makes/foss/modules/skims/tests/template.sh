# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME
  local host="127.0.0.1"
  local port="8022"

  sops_export_vars __argSecretsFile__ "INTEGRATES_API_TOKEN" \
    && if test '__argShouldMock__' == '1'; then
      DAEMON=true integrates-back dev \
        && DAEMON=true POPULATE=false integrates-db \
        && DAEMON=true POPULATE=false integrates-storage \
        && DAEMON=true integrates-cache \
        && for data in '__argDbData__/'*'.json'; do
          echo "[INFO] Writing data from: ${data}" \
            && aws dynamodb batch-write-item \
              --endpoint-url "http://${host}:${port}" \
              --request-items "file://${data}" \
            || return 1
        done
    fi \
    && CI_COMMIT_REF_NAME="$(get_abbrev_rev "${PWD}" HEAD)"
}

main "${@}"
