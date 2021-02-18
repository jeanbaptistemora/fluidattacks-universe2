# shellcheck shell=bash

function dump {
      cat __envForces__ > makes/profiles/forces.sh \
  &&  cat __envMelts__ > makes/profiles/melts.sh \
  &&  cat __envReviews__ > makes/profiles/reviews.sh \
  &&  cat __envSkims__ > makes/profiles/skims.sh \
  &&  cat __envSorts__ > makes/profiles/sorts.sh \
  &&  cat __envHacker__ > makes/profiles/hacker.sh
}

dump "${@}"
