# shellcheck shell=bash

function main {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  source __argPythonEnv__/template \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      PROD_COMMON_AWS_ACCESS_KEY_ID \
      PROD_COMMON_AWS_SECRET_ACCESS_KEY \
    && AWS_ACCESS_KEY_ID="${PROD_COMMON_AWS_ACCESS_KEY_ID}" \
    && AWS_SECRET_ACCESS_KEY="${PROD_COMMON_AWS_SECRET_ACCESS_KEY}" \
    && python3 __argScript__ "${@}"

}

main "${@}"
