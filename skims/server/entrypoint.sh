# shellcheck shell=bash

function main {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY

  aws_login_prod skims \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
    && pushd '__argSkims__' \
    && python3 \
      -m celery \
      -A server \
      worker \
      --concurrency 2 \
      -l INFO \
    && popd || return
}

main "${@}"
