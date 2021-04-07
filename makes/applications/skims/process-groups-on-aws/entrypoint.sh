# shellcheck shell=bash

function list_checks {
  local results

      results="$(mktemp)" \
  &&  grep -oP \
        '[A-Z0-9_]+(?=: FindingMetadata)' \
        'skims/skims/model/core_model.py' \
        > "${results}" \
  &&  echo "${results}"
}

function main {
      aws_login_prod 'skims' \
  &&  mapfile -t checks < "$(list_checks)" \
  &&  echo "[INFO] Findings to execute: ${checks[*]}" \
  &&  use_git_repo_services \
    &&  shopt -s nullglob \
    &&  for group in "groups/"*
        do
              group="$(basename "${group}")" \
          &&  for check in "${checks[@]}"
              do
                    skims-process-group-on-aws "${group}" "${check}" \
                ||  return 1
              done \
          ||  return 1
        done \
    &&  shopt -u nullglob \
  &&  popd \
  ||  return 1
}

main "${@}"
