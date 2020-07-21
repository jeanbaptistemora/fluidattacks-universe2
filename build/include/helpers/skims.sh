# shellcheck shell=bash

function helper_skims_compute_version {
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

function helper_skims_install_base_dependencies {
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
