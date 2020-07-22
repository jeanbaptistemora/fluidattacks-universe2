# shellcheck shell=bash
function helper_forces_install_base_dependencies {
      pushd forces/ \
    &&  { test -e poetry.lock || poetry install; } \
  &&  popd \
  ||  return 1
}
