#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --cores 0
#!   nix-shell --keep ENCRYPTION_KEY
#!   nix-shell --keep ENCRYPTION_KEY_PROD
#!   nix-shell --max-jobs auto
#!   nix-shell --option restrict-eval false
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell --show-trace
#!   nix-shell shell.nix
#  shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source ./build/include/helpers.sh
source ./.envrc.public

function prepare_environment {
  export PATH
  export PYTHONPATH
  export PERSISTENT_DIR
  export SITE_PACKAGES
  export TEMP_DIR
  export TEMP_FILE

  # Ephemeral variables
  #   they are different on every invocation and therefore every
  #   Python Package will be reinstalled into a pristine
  #   environment on each execution.
  # Packages placed here will be isolated from the user installed ones
  #   much like a virtual-envivironment (except that it's not)
  TEMP_FILE=$(mktemp)
  TEMP_DIR=$(mktemp -d)
  SITE_PACKAGES=$(mktemp -d)
  mkdir "${SITE_PACKAGES}/bin"

  # Persistent dir structure where files will be stored.
  #   use these to save things that are expensive to build/fetch
  #   like repositories
  # ALWAYS treat this files without side effects:
  #   - the first invocation where ${PERSISTENT_DIR} does not exist must work
  #   - the second and later must not fail due to garbage of previous invocations
  PERSISTENT_DIR="${PWD}/.tmp"
  mkdir -p "${PERSISTENT_DIR}"

  # Set the PYTHONPATH to the nix-created environment
  PYTHONPATH="${PYTHONPATH}:${pyPkgFluidassertsBasic}/site-packages"
  PYTHONPATH="${PYTHONPATH}:${pyPkgGroupTest}/site-packages"
  PYTHONPATH="${PYTHONPATH}:${pyPkgGitPython}/site-packages"
  PYTHONPATH="${PYTHONPATH}:${pyPkgMandrill}/site-packages"
  PYTHONPATH="${PYTHONPATH}:${SITE_PACKAGES}"

  # Set on PATH scripts installed with python
  PATH="${PATH}:${pyPkgFluidassertsBasic}/site-packages/bin"
  PATH="${PATH}:${pyPkgGroupTest}/site-packages/bin"
  PATH="${PATH}:${SITE_PACKAGES}/bin"
  chmod +x "${pyPkgFluidassertsBasic}/site-packages/bin/asserts"
  chmod +x "${pyPkgGroupTest}/site-packages/bin/pytest"
}

#
# CLI flags / Gitlab CI jobs
#

function release_to_docker_hub {
  with_production_secrets

  ensure_binary 'docker'
  ensure_environment_variables \
    DOCKER_HUB_URL \
    DOCKER_HUB_USER \
    DOCKER_HUB_PASS

  docker login "${DOCKER_HUB_URL}" \
    --username "${DOCKER_HUB_USER}" \
    --password-stdin \
    <<< "${DOCKER_HUB_PASS}"

  function build {
    local image_name="${1}"
    local target_name="${2}"
    local file="${3}"
    docker build --tag "${image_name}" --target "${target_name}" -f "${file}" .
    docker push "${image_name}"
  }

  build 'fluidattacks/asserts:debian-light' 'light' 'debian.Dockerfile'
  build 'fluidattacks/asserts:debian-full'  'full'  'debian.Dockerfile'
  build 'fluidattacks/asserts:debian'       'full'  'debian.Dockerfile'
}

function release_to_pypi {
  with_production_secrets

  ensure_environment_variables \
    TWINE_USERNAME \
    TWINE_PASSWORD \

  twine check  './result.build_fluidasserts_release/'*
  twine upload './result.build_fluidasserts_release/'*
}

function send_new_version_mail {
  with_production_secrets

  ensure_environment_variables \
    CI_COMMIT_BEFORE_SHA \
    CI_COMMIT_SHA        \
    MANDRILL_APIKEY      \

  ./build/scripts/send_mail.py
}

function test_fluidasserts {
  with_development_secrets

  local marker_name="${1}"

  function mocks_ctl {
    local action="${1}"
    local marker_name="${2}"

    ensure_binary 'docker'

    pytest \
        -m "${action}" \
        --asserts-module "${marker_name}" \
        --capture=no \
        --no-cov \
      "test/test_others_${action}.py"
  }

  function compute_needed_test_modules_for {
    grep -lrP "'${1}'" "test/test_"*
  }

  function execute_tests_for {
    local marker_name="${1}"
    local test_modules

    mapfile -t test_modules \
      < <(compute_needed_test_modules_for "${marker_name}")

    pytest \
        --cov-branch \
        --asserts-module "${marker_name}" \
        --random-order-bucket=global \
      "${test_modules[@]}"
  }

                  mocks_ctl prepare  "${marker_name}"
  execute_on_exit mocks_ctl shutdown "${marker_name}"

  execute_tests_for "${marker_name}"
}

function cli {
  local command

  # Export vars to the current environment:
  #   --env var1_name var1_value --env var2_name var2_value ...
  while true
  do
    if test "${1:-}" = '--env'
    then
      shift 1
      echo "/nix/env: setting environment var ${1:-}"
      export "${1:-}"="${2:-}"
      shift 2 || (
        echo 'Expected: --env var_name var_value' && exit 1
      )
    else
      break
    fi
  done

  # Dispatch a group of commands based on the provided arguments
  # '--xxx' will call 'xxx' function
  # '-c' will execute a single command and exit
  case "${1:-}" in
    '-c') {
        eval "${2:-}";
        return 0;
      };;
    *) {
        # Remove initial dashes: '--aaa-bbb' -> 'aaa-bbb'
        command="${1#*--}"
        shift 1
        # Replace dash with underscore: 'aaa-bbb' -> 'aaa_bbb'
        "${command//-/_}" "${@}"
        return 0;
      };;
  esac
}

prepare_environment
cli "${@}"
