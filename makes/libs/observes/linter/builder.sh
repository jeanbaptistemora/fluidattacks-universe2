# shellcheck shell=bash

function list_packages {
    find "${envSrc}" \
        -mindepth 2 -maxdepth 2 \
        -name '__init__.py' \
        -printf '%h\n'
}

function main {
  local pkgs

      pkgs=$(mktemp) \
  &&  list_packages > "${pkgs}" \
  &&  while read -r pkg
      do
            lint_python_module "${pkg}" \
        ||  return 1
      done < "${pkgs}" \
  &&  touch "${out}"
}

main "${@}"
