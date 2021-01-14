# shellcheck shell=bash

source "${envSetupSortsDevelopment}"
source "${envSetupSortsRuntime}"
source "${envBashLibLintPython}"

function list_packages {
      target="${PWD}/test" \
  &&  copy "${envSrcSortsTest}" "${target}" \
  &&  echo "${target}" \
  &&  target="${PWD}/training" \
  &&  copy "${envSrcSortsTraining}" "${target}" \
  &&  echo "${target}" \
  &&  find "${envSrcSortsSorts}" -mindepth 1 -maxdepth 1 -type d \
        | while read -r folder
          do
                target="${PWD}/$(basename "${folder}")" \
            &&  copy "${folder}" "${target}" \
            &&  echo "${target}" \
            ||  return 1
          done
}

function main {
  local pkgs

      pkgs=$(mktemp) \
  &&  list_packages > "${pkgs}" \
  &&  while read -r pkg
      do
            lint_python "${pkg}" \
        ||  return 1
      done < "${pkgs}" \
  &&  success
}

main "${@}"
