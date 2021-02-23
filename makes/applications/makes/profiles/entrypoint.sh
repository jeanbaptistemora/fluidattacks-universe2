# shellcheck shell=bash

function dump {
      cat __envAsserts__ > makes/profiles/asserts.sh \
  &&  cat __envForces__ > makes/profiles/forces.sh \
  &&  cat __envIntegratesBack__ > makes/profiles/integrates-back.sh \
  &&  cat __envIntegratesCache__ > makes/profiles/integrates-cache.sh \
  &&  cat __envIntegratesDb__ > makes/profiles/integrates-db.sh \
  &&  cat __envIntegratesStorage__ > makes/profiles/integrates-storage.sh \
  &&  cat __envMelts__ > makes/profiles/melts.sh \
  &&  cat __envReviews__ > makes/profiles/reviews.sh \
  &&  cat __envSkims__ > makes/profiles/skims.sh \
  &&  cat __envSorts__ > makes/profiles/sorts.sh \
  &&  cat __envHacker__ > makes/profiles/hacker.sh
}

dump "${@}"
