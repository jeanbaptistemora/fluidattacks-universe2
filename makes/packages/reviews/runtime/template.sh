# shellcheck shell=bash

function reviews {
  python3.8 '__envSrcReviews__/cli/__init__.py' "$@"
}
