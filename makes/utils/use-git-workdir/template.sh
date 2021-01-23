# shellcheck shell=bash

function use_git_workdir {
  local startdir="${PWD}"
  local workdir="${startdir}/../product.workdir"

      echo '[INFO] Creating a pristine git workdir' \
  &&  if test -e "${workdir}"
      then
            echo "[INFO] Removing old git workdir: ${workdir}" \
        &&  __envGit__ worktree remove -f "${workdir}"
      fi \
  &&  __envGit__ worktree add -f "${workdir}" "${CI_COMMIT_REF_NAME}" \
  &&  pushd "${workdir}" \
  ||  return 1
}
