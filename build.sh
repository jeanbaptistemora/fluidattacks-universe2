#! /usr/bin/env bash

source ./build-src/include/generic/shell-options.sh

#
# Functions
#

function execute {
  # Build a derivation from the provided expression without creating a symlink
  nix-build \
      --attr "${1}" \
      --cores 0 \
      --max-jobs auto \
      --no-out-link \
      --option restrict-eval false \
      --option sandbox false \
    ./build-src/main.nix
}

function execute_and_link {
  # Build a derivation from the provided expression and create a symlink to the nix store
  nix-build \
      --attr "${1}" \
      --cores 0 \
      --max-jobs auto \
      --out-link "${2:-nix-result}" \
      --option restrict-eval false \
      --option sandbox false \
    ./build-src/main.nix
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
      'lint_nix_code'
      'lint_python_code_bandit'
      'lint_shell_code'
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
  # Set the current system to use the cache
  cachix use "${CACHIX_CACHE_NAME}" 1>&2
}

function use_cachix_if_dev_branch {
  # Set cachix if we are in a branch that is not master
  test "${CURRENT_BRANCH}" != 'master' \
    && use_cachix \
    || :
}

function push_to_cachix {
  # Pipe an execute to this function in order to populate the cache
  cachix push --compression-level 9 "${CACHIX_CACHE_NAME}"
}

#
# Gitlab Jobs
#

function job_lint_nix_code {
  use_cachix_if_dev_branch
  execute lintNixCode
}

function job_lint_python_code_bandit {
  use_cachix_if_dev_branch
  execute lintPythonCodeBandit
}

function job_lint_shell_code {
  use_cachix_if_dev_branch
  execute lintPythonCodeBandit
}

function job_doc {
  # Build our hosted GitLab Pages
  use_cachix

  execute_and_link generateDoc doc-result

  ./build-src/shell.sh -c 'rm -rf public; mkdir public'
  ./build-src/shell.sh -c 'cp -r --no-preserve=mode,ownership doc-result/* public'

  echo 'Check the docs at public/index.html!'
  rm -f doc-result
}

function job_doc_test {
  job_doc
}

function job_populate_caches {
  use_cachix_if_dev_branch

  # Execute the 'populate_caches' job in the .gitlab-ci.yml
  (
    job_lint_nix_code
    job_lint_python_code_bandit
    job_lint_shell_code
    execute pyPkgFluidasserts
    execute pyPkgGitFame
    execute pyPkgSphinx
  ) | push_to_cachix
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
      echo "Use:"
      echo "  ${0} --branch [branch_name]"
      echo "  ${0} --job    [job_name]"
      echo
      echo "List of [job_name]:"
      set | grep -oP '^job_[a-z_]+' | sed -e 's/job_/  /g;s/_/-/g' | sort
      return 1
    elif test "${token}" = '--branch'
    then
      shift 1 || break
      export CI_COMMIT_REF_NAME="${1}"
    elif test "${token}" = '--job'
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

  # Execute the respective job functions
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
