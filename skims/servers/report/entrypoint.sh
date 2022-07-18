# shellcheck shell=bash

function main {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

  ensure_gitlab_env_vars \
    INTEGRATES_API_TOKEN \
    PROD_SKIMS_AWS_ACCESS_KEY_ID \
    PROD_SKIMS_AWS_SECRET_ACCESS_KEY \
    && AWS_ACCESS_KEY_ID="${PROD_SKIMS_AWS_ACCESS_KEY_ID}" \
    && AWS_SECRET_ACCESS_KEY="${PROD_SKIMS_AWS_SECRET_ACCESS_KEY}" \
    && python3 -m celery --workdir __argSkims__ -A server worker -l INFO
}

main "${@}"
