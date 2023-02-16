# shellcheck shell=bash

# Make subprocesses orphan when running in CI
# in order to avoid https://gitlab.com/gitlab-org/gitlab-runner/-/issues/2880
function daemonize {
  if test -n "${CI:-}"; then
    DAEMON=true "${@}" < /dev/null &> /dev/null &
  else
    DAEMON=true "${@}" &
  fi
}

function main {
  : \
    && daemonize dynamodb \
    && daemonize opensearch \
    && wait \
    && if [ "${DAEMON:-}" = "true" ]; then
      daemonize integrates-streams dev
    else
      integrates-streams dev
    fi

}

main "${@}"
