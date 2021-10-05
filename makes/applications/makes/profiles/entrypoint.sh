# shellcheck shell=bash

function dump {
  : && cat __envIntegratesBack__ > makes/profiles/integrates-back.sh \
    && cat __envSkims__ > makes/profiles/skims.sh
}

dump "${@}"
