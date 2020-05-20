#! /usr/bin/env bash

source ./build/include/generic/shell-options.sh
source ./build/include/constants.sh
source ./build/include/helpers.sh

#
# Functions
#

function build {
  # Build a derivation from the provided expression without creating a symlink
  local derivation_name="${1}"
  nix-build \
      --attr "${derivation_name}" \
      --cores "${NIX_BUILD_CORES}" \
      --max-jobs "${NIX_BUILD_MAX_JOBS}" \
      --no-out-link \
      --option restrict-eval false \
      --option sandbox false \
      --show-trace \
    ./build/main.nix
}

function build_and_link {
  # Build a derivation from the provided expression and create a symlink to the nix store
  local derivation_name="${1}"
  local derivation_output_name="${2}"

  nix-build \
      --attr "${derivation_name}" \
      --cores "${NIX_BUILD_CORES}" \
      --max-jobs "${NIX_BUILD_MAX_JOBS}" \
      --out-link "${derivation_output_name}" \
      --option restrict-eval false \
      --option sandbox false \
      --show-trace \
    ./build/main.nix
}

function build_and_link_x {
  local derivation_name="${1}"
  local derivation_output_name="${2}"
  build_and_link "${derivation_name}" "${derivation_output_name}"
  chmod +x "${derivation_output_name}"
}

function ensure_dependencies {
  # Make sure that nix is installed
  echo ---
  nix --version \
    || (
      echo 'Please install nix: $ curl https://nixos.org/nix/install | sh'
      return 1
    )

  # Make sure that git is installed
  git --version \
    || (
      echo 'Please install git'
      return 1
    )

  # Make sure that cachix is installed
  (nix-env -q | grep 'cachix') \
    || nix-env -iA 'cachix' -f 'https://cachix.org/api/v1/install'

}

function set_cachix_authtoken {
  # Set the cachix Auth Token
  echo ---
  test -n "${CACHIX_AUTH_TOKEN:-}" \
    && cachix authtoken "${CACHIX_AUTH_TOKEN}" \
    || echo 'cachix auth token not present'
}

function set_environment_info {
  # Set the current branch and jobs that should run as environment vars
  local current_job
  local default_branch='unknown-branch'
  export CURRENT_BRANCH
  export CURRENT_JOBS

  test -n "${CI_JOB_NAME:-}" \
    && current_job="${CI_JOB_NAME}" \
    || current_job="__undefined__"

  test -n "${CI_COMMIT_REF_NAME:-}" \
    && CURRENT_BRANCH="${CI_COMMIT_REF_NAME}" \
    || CURRENT_BRANCH=$(
      git rev-parse --abbrev-ref HEAD 2>/dev/null \
        || echo "${default_branch}")

  test "${current_job}" = '__undefined__' \
    && CURRENT_JOBS=(
      'demo_fluidasserts_output'
    ) \
    || CURRENT_JOBS=(
      "${current_job}"
    )

  echo ---
  echo "branch:      ${CURRENT_BRANCH}"
  echo "jobs to run: ${CURRENT_JOBS[*]}"
  echo ---
  echo 'sourcing: .envrc.public'
  source .envrc.public
}

function set_ephemeral_git {
  echo ---
  test -e .tmp || mkdir .tmp
  git log -1 --format=%B HEAD &> .tmp/git-last-commit-msg
  cat .tmp/git-last-commit-msg
}

function use_cachix {
  export IS_CACHIX_SET

  # Set the current system to use the cache (if not already set)
  if test "${IS_CACHIX_SET:-}" = "${NO}"
  then
    IS_CACHIX_SET="${YES}"
    cachix use "${CACHIX_CACHE_NAME}" 1>&2
  fi
}

function use_cachix_if_dev_branch {
  # Set cachix if we are in a branch that is not master
  test "${CURRENT_BRANCH}" != 'master' \
    && use_cachix \
    || :
}

function push_to_cachix {
  # Pipe a build to this function in order to populate the cache
  cachix push --compression-level 9 "${CACHIX_CACHE_NAME}"
}

#
# Gitlab Jobs
#

function job_demo_fluidasserts_output {
  use_cachix
  build demoFluidassertsOutput
}

function cli {
  # A small interface to parse arguments like --job and --branch.
  #   with this you can simulate the remote CI for after-master jobs
  #   or run only a subset of the pre-master jobs.

  while true
  do
    token="${1:-}"

    if test -z "${token}"
    then
      return 0
    elif test "${token}" = '-h' || test "${token}" = '--help'
    then
      echo "Use of ${0}:"
      echo "  -b, --branch  [branch_name] simulate being in another branch"
      echo "  -h, --help                  print this message and exit"
      echo "  -j, --job     [job_name]    execute a particular job"
      echo
      echo "Available jobs:"
      set | grep -oP '^job_[a-z_]+' | sed -e 's/job_/  /g;s/_/-/g' | sort
      return 1
    elif test "${token}" = '-b' || test "${token}" = '--branch'
    then
      shift 1 || break
      export CI_COMMIT_REF_NAME="${1}"
    elif test "${token}" = '-j' || test "${token}" = '--job'
    then
      shift 1 || break
      # replace dash with underscore
      export CI_JOB_NAME="${1//-/_}"
    else
      echo "Unrecognized option: ${token}"
      return 1
    fi

    shift 1 || return 0
  done
}

function main {
  ensure_dependencies

  set_ephemeral_git
  set_environment_info
  set_cachix_authtoken

  # Run the respective job functions
  for job_name in "${CURRENT_JOBS[@]}"
  do
    echo ---
    echo "job:   ${job_name}"
    echo ---
    "job_${job_name}"
  done
}

cli "${@}"

main
