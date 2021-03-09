# shellcheck shell=bash

function list_packages {
    local srcPath="${1}"

    find "${srcPath}" \
        -mindepth 2 -maxdepth 2 \
        -name '__init__.py' \
        -printf '%h\n'
}

function observes_generic_lint {
  local srcPath="${1}"
  local pkgs

      pkgs=$(mktemp) \
  &&  list_packages "${srcPath}" > "${pkgs}" \
  &&  while read -r pkg
      do
            lint_python_module "${pkg}" \
        ||  return 1
      done < "${pkgs}" \
  &&  touch "${out}"
}
