# shellcheck shell=bash

function main {

  local package_path=__argIntegratesPackage__

  package_name="$(basename "__argIntegratesPackage__")" \
    && source __argIntegratesBackEnv__/template dev \
    && info Running mypy over: "${package_path}", package "${package_name}" \
    && if test -e "${package_path}/py.typed"; then
      error This is not a mypy package, py.typed missing
    fi \
    && tmpdir="$(mktemp -d)" \
    && copy "${package_path}" "${tmpdir}/${package_name}" \
    && pushd "${tmpdir}" \
    && mypy --config-file __argSettingsMypy__ "${package_name}"

}

main "${@}"
