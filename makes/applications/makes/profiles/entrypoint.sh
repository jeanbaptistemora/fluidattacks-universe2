# shellcheck shell=bash

function dump {
  : && cat __envIntegratesBack__ > makes/profiles/integrates-back.sh \
    && cat __envIntegratesCache__ > makes/profiles/integrates-cache.sh \
    && cat __envIntegratesDb__ > makes/profiles/integrates-db.sh \
    && cat __envIntegratesStorage__ > makes/profiles/integrates-storage.sh \
    && cat __envSkims__ > makes/profiles/skims.sh
}

dump "${@}"
