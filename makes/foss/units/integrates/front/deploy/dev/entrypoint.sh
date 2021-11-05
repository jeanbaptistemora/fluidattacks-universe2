# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME

  : \
    && if test -z "${CI_COMMIT_REF_NAME:-}"; then
      CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)"
    fi \
    && deploy dev_new development "${CI_COMMIT_REF_NAME}"
}

main "${@}"
