# shellcheck shell=bash

function get_touched_files_last_commit {
  export CI_COMMIT_BEFORE_SHA
  export CI_COMMIT_SHA

  git diff --name-only "${CI_COMMIT_BEFORE_SHA}" "${CI_COMMIT_SHA}" \
    | while read -r path
      do
        ! test -e "${path}" || echo "${path}"
      done
}

function has_any_file_changed {
  local canon_file_a
  local canon_file_b
  local file
  local files=( "$@" )
  local touched_files

      touched_files="$(mktemp)" \
  &&  get_touched_files_last_commit > "${touched_files}" \
  &&  while read -r touched_file
      do
        for file in "${files[@]}"
        do
              canon_file_a=$(readlink -f "${touched_file}") \
          &&  canon_file_b=$(readlink -f "${file}") \
          &&  if [[ "${canon_file_a}" == "${canon_file_b}"* ]]
              then
                echo "${canon_file_a}"
                echo "${canon_file_b}"
                return 0
              else
                continue
              fi
        done || :
      done < "${touched_files}" \
  &&  return 1
}

function use_git_repo {
  local source="${1}"
  local target="${2}"
  local rev="${3:-HEAD}"

  if test -e "${target}"
  then
        echo "[INFO] Updating local repository copy at: ${target}" \
    &&  pushd "${target}" \
      &&  __envGit__ remote set-url origin "${source}" \
      &&  __envGit__ fetch \
      &&  __envGit__ reset --hard "${rev}" \
    ||  return 1
  else
        echo "[INFO] Creating local repository copy at: ${target}" \
    &&  __envGit__ clone --single-branch "${source}" "${target}" \
    &&  pushd "${target}" \
      &&  __envGit__ reset --hard "${rev}" \
    ||  return 1
  fi
}

function use_git_repo_services {
  export GITLAB_API_TOKEN
  export GITLAB_API_USER

  use_git_repo \
    "https://${GITLAB_API_USER}:${GITLAB_API_TOKEN}@gitlab.com/fluidattacks/services.git" \
    "${PWD}/../services"
}
