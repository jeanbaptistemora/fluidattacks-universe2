# shellcheck shell=bash

source '__envUtilsBashLibAws__'
source '__envUtilsBashLibGit__'

function main {
      aws_login_prod 'skims' \
  &&  use_git_repo_services \
    &&  shopt -s nullglob \
    &&  for group in "groups/"*
        do
              group="$(basename "${group}")" \
          &&  echo "[INFO] Scheduling ${group}" \
          &&  __envSkimsProcessGroupOnAws__ "${group}" \
          ||  return 1
        done \
    &&  shopt -u nullglob \
  &&  popd \
  ||  return 1
}

main "${@}"
