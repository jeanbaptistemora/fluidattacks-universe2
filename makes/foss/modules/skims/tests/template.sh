# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME

  require_env_var INTEGRATES_API_TOKEN \
    && CI_COMMIT_REF_NAME="$(get_abbrev_rev "${PWD}" HEAD)"
}

main "${@}"
