#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --cores 0
#!   nix-shell --keep CI_REGISTRY_USER
#!   nix-shell --keep CI_REGISTRY_PASSWORD
#!   nix-shell --max-jobs auto
#!   nix-shell --option restrict-eval false
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell --show-trace
#!   nix-shell shell.nix
#  shellcheck shell=bash

# shellcheck disable=SC2154
# shellcheck source=./build/include/generic/shell-options.sh
source "${srcGenericShellOptions}"
source "${srcHelpers}"

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

function job_all {
  local function_to_call

  # Execute all job functions except this mere one
  helper_list_declared_jobs | while read -r function_to_call
  do
    echo "[INFO] Executing function: ${function_to_call}"
    test "${function_to_call}" = "job_all" \
      || "${function_to_call}" \
      || return 1
  done
}

function job_deploy_nix_docker_image {
  local image="${CI_REGISTRY_IMAGE}:nix"

    echo "[INFO] Login in: ${CI_REGISTRY}" \
  && docker login \
      --username "${CI_REGISTRY_USER}" \
      --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  && echo "[INFO] Pulling: ${image}" \
  && docker pull "${image}" || true \
  && echo "[INFO] Building: ${image}" \
  && docker build --tag "${image}" --file './build/Dockerfile' '.' \
  && echo "[INFO] Pushing: ${image}" \
  && docker push "${image}"
}

function job_lint_build_code {
      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find 'build' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2154, {} + \
  && echo '[OK] Shell code is compliant' \
  && hadolint build/Dockerfile \
  && echo '[OK] Dockerfiles are compliant'
}

function cli {
  local function_to_call

  function_to_call="${1:-}"

  if test -z "${function_to_call}"
  then
    echo
    echo "Use: ./build.sh [job-name]"
    echo
    echo 'List of jobs:'
    helper_list_declared_jobs | sed -e 's/job_/  * /g'
    return 1
  else
    echo
    prepare_environment_variables
    prepare_workdir
    echo "[INFO] Executing function: job_${function_to_call}"
    if "job_${function_to_call}"
    then
      echo
      echo "Successfully executed: ${function_to_call}"
      echo '  Congratulations!'
      return 0
    else
      echo
      echo 'We have found some problems with your commit'
      echo '  You can replicate this output locally with:'
      echo "    serves $ ./build.sh ${function_to_call}"
      return 1
    fi
  fi
}

cli "${@}"
