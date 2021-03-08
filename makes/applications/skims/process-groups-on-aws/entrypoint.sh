# shellcheck shell=bash

function main {
      aws_login_prod 'skims' \
  &&  use_git_repo_services \
    &&  shopt -s nullglob \
    &&  for group in "groups/"*
        do
              group="$(basename "${group}")" \
          &&  echo "[INFO] Scheduling ${group}" \
          &&  skims-process-group-on-aws "${group}" \
          ||  return 1
        done \
    &&  shopt -u nullglob \
  &&  popd \
  ||  return 1
}

main "${@}"
