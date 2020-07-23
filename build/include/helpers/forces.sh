# shellcheck shell=bash

function helper_forces_compute_version {
  poetry run python -c 'if True:
    import time
    now=time.gmtime()
    minutes_month=(
      (now.tm_mday - 1) * 1440
      + now.tm_hour * 60
      + now.tm_min
    )
    print(time.strftime(f"%y.%m.{minutes_month}"))
  '
}

function helper_forces_install_base_dependencies {
      pushd forces/ \
    &&  { test -e poetry.lock || poetry install; } \
  &&  popd \
  ||  return 1
}
