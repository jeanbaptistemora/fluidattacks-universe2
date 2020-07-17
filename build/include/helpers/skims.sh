# shellcheck shell=bash

function helper_skims_install_dependencies {
      pushd skims/ \
    &&  { test -e poetry.lock || poetry install; } \
  &&  popd \
  ||  return 1
}

function helper_skims_force_install {
      pushd skims/ \
    &&  poetry update \
    &&  poetry install \
  &&  popd \
  ||  return 1
}
