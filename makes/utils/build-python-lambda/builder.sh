# shellcheck shell=bash

function main {
  local workdir="${PWD}/workdir"
  local lambda="${workdir}/lambda.zip"

      mkdir "${workdir}" \
  &&  pushd "${envRequirements}/lib/python"*'/site-packages' \
    &&  zip --recurse-paths -9 "${lambda}" . \
  &&  popd \
  &&  pushd "${envSource}" \
    &&  zip --grow --recurse-paths -9 "${lambda}" . \
  &&  popd \
  &&  mv "${lambda}" "${out}" \
  ||  return 1
}

main "${@}"
