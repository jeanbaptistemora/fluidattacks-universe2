# shellcheck shell=bash

function list_packages {
  local srcPath="${1}"

  find "${srcPath}" \
    -mindepth 2 -maxdepth 2 \
    -name '__init__.py' \
    -printf '%h\n'
}

function list_import_confs {
  local srcPath="${1}"

  find "${srcPath}" \
    -maxdepth 2 \
    -name 'setup.imports.cfg' \
    -printf '%h\n'
}

function imports_lint {
  local pkgs

  pkgs=$(mktemp) \
    && list_import_confs "${srcPath}" > "${pkgs}" \
    && while read -r pkg; do
      echo "[INFO] Lint imports at ${pkg}" \
        && lint_python_imports "${pkg}/setup.imports.cfg" "${pkg}" \
        || return 1
    done < "${pkgs}"
}

function pkg_lint {
  local pkgs

  pkgs=$(mktemp) \
    && list_packages "${srcPath}" > "${pkgs}" \
    && while read -r pkg; do
      lint_python_package "${pkg}" \
        || return 1
    done < "${pkgs}"
}

function observes_generic_lint {
  local srcPath="${1}"

  imports_lint \
    && pkg_lint \
    && touch "${out}"
}

function observes_generic_lint_pkg_container {
  local srcPath="${1}"
  local pkgs

  pkgs=$(mktemp) \
    && lint_python_imports "${srcPath}/setup.imports.cfg" "${srcPath}" "False" \
    && touch "${out}"
}
