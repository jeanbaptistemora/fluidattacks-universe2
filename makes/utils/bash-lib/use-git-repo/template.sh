# shellcheck shell=bash

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

  helper_common_use_repo \
    "https://${GITLAB_API_USER}:${GITLAB_API_TOKEN}@gitlab.com/fluidattacks/services.git" \
    "${PWD}/../services"
}
