# shellcheck shell=bash

function prepare_environment_variables {
    echo "[INFO] Sourcing .envrc.public" \
  && source './.envrc.public'
}

function prepare_workdir {
  export WORKDIR
  export PRE_COMMIT_HOME

    WORKDIR=$(readlink -f "${PWD}/../serves.ephemeral") \
  && echo '[INFO] Creating a pristine workdir' \
  && rm -rf "${WORKDIR}" \
  && echo '[INFO] Adding a pristine workdir' \
  && cp -r . "${WORKDIR}"
}
