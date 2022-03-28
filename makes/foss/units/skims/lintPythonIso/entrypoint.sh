# shellcheck shell=bash

function main {

  local package_path=__argSkimsPackage__

  package_name="$(basename "__argSkimsPackage__")" \
    && info Running mypy over: "${package_path}", package "${package_name}" \
    && tmpdir="$(mktemp -d)" \
    && copy "${package_path}" "${tmpdir}/skims" \
    && pushd "${tmpdir}" \
    && export MYPYPATH=${tmpdir}/skims \
    && mypy --follow-imports=normal --namespace-packages \
      --explicit-package-bases --config-file __argSettingsMypy__ "${tmpdir}/skims"

}

main "${@}"
