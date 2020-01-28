#! /usr/bin/env bash

source ./build-src/include/generic/shell-options.sh
source ./build-src/include/constants.sh
source ./build-src/include/helpers.sh

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
    ./build-src/main.nix
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
    ./build-src/main.nix
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
      'lint_fluidasserts_code'
      'lint_fluidasserts_test_code'
      'lint_nix_code'
      'lint_shell_code'
      'lint_with_bandit'
      'test_commit_message'
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

function job_build_fluidasserts_release {
  use_cachix_if_dev_branch
  build_and_link buildFluidassertsRelease result-build_fluidasserts_release
}

function job_demo_fluidasserts_output {
  use_cachix_if_dev_branch
  build demoFluidassertsOutput
}

function job_lint_fluidasserts_code {
  use_cachix_if_dev_branch
  build lintFluidassertsCode
}

function job_lint_fluidasserts_test_code {
  use_cachix_if_dev_branch
  build lintFluidassertsTestCode
}

function job_lint_nix_code {
  use_cachix_if_dev_branch
  build lintNixCode
}

function job_lint_shell_code {
  use_cachix_if_dev_branch
  build lintShellCode
}

function job_lint_with_bandit {
  use_cachix_if_dev_branch
  build lintWithBandit
}

function job_pages {
  # Build our hosted GitLab Pages
  use_cachix

  build_and_link generateDoc result-pages

  ./build-src/shell.sh -c 'rm -rf public; mkdir public'
  ./build-src/shell.sh -c 'cp -r --no-preserve=mode,ownership result-pages/* public'

  echo 'Check the docs at public/index.html!'
  rm -f result-pages
}

function job_populate_caches {
  use_cachix_if_dev_branch

  (
    job_demo_fluidasserts_output
    job_lint_fluidasserts_code
    job_lint_fluidasserts_test_code
    job_lint_nix_code
    job_lint_shell_code
    job_lint_with_bandit
    job_test_commit_message
    build fluidassertsDependenciesCache
    build nodePkgCommitlint
    build pyPkgFluidassertsBasic
    build pyPkgGitFame
    build pyPkgGitPython
    build pyPkgGroupLint
    build pyPkgGroupTest
    build pyPkgMandrill
    build pyPkgSphinx
  ) | push_to_cachix
}

function job_release_to_pypi {
  local runner_file
  local runner_name
  use_cachix_if_dev_branch

  runner_name='ephemeral-runner.release_to_pypi'
  runner_file="./${runner_name}"

  build_and_link_x releaseToPyPi "${runner_name}"
  "${runner_file}"
}

function job_release_to_docker_hub {
  local runner_file
  local runner_name
  use_cachix_if_dev_branch

  runner_name='ephemeral-runner.release_to_docker_hub'
  runner_file="./${runner_name}"

  build_and_link_x releaseToDockerHub "${runner_name}"
  "${runner_file}"
}

function job_send_new_version_mail {
  use_cachix

  ./build-src/shell.sh \
    --env 'CI_COMMIT_SHA'        "${CI_COMMIT_SHA:-}"        \
    --env 'CI_COMMIT_BEFORE_SHA' "${CI_COMMIT_BEFORE_SHA:-}" \
    --send-new-version-mail
}

function job_test_commit_message {
  use_cachix_if_dev_branch
  build testCommitMessage
}

function job_test_api {
  # Just execute all markers by calling the respective distpatch functions
  for marker in "${TEST_MARKERS[@]}"
  do
    test "${marker}" = "all" || "job_test_api_${marker}"
  done
}

function _job_test_api__generic_dispatcher {
  local caller_function
  local runner_file
  local runner_name
  local derivation_name

  # Inspect the stack and get the name of the function that called this function
  caller_function="${FUNCNAME[1]}"

  # The caller function without the 'job_test_api_' prefix
  runner_name="${caller_function#job_test_api_}"

  # The caller function but 'TitleCase' instead of 'title_case'
  derivation_name=$(camel_case_to_title_case "${runner_name}")

  # Add a prefix to make the distintion
  derivation_name="testFluidasserts${derivation_name}"
  runner_name="ephemeral-runner.test_api_${runner_name}"
  runner_file="${PWD}/${runner_name}"

  # Build the derivation and save the output as an executable file
  build_and_link_x "${derivation_name}" "${runner_name}"

  "${runner_file}"
}

# Populate the context with functions for every test marker
for marker in "${TEST_MARKERS[@]}"
do
  eval "function job_test_api_${marker} { _job_test_api__generic_dispatcher; }"
done

function job_test_doc {
  job_pages
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
