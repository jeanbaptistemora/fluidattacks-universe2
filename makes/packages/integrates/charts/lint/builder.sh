# shellcheck shell=bash

function main {
      pushd "${envGraphsSrc}" \
    &&  eslint --config .eslintrc . \
  &&  popd \
  &&  lint_python_package "${envChartsSrc}" \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
