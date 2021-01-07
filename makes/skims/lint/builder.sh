# shellcheck shell=bash

source "${envSetupSkimsRuntime}"
source "${envBashLibLintPython}"

function list_packages {
      target="${PWD}/test" \
  &&  copy "${envSrcSkimsTest}" "${target}" \
  &&  echo "${target}" \
  &&  find "${envSrcSkimsSkims}" -mindepth 1 -maxdepth 1 -type d \
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
  local success='true'

      pkgs=$(mktemp) \
  &&  list_packages > "${pkgs}" \
  &&  while read -r pkg
      do
            lint_python "${pkg}" \
        ||  success='false'
      done < "${pkgs}" \
  &&  test "${success}" = 'true' \
  &&  success
}

main "${@}"
