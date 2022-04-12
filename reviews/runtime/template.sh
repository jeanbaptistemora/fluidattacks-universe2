# shellcheck shell=bash

function reviews {
  python3.8 '__argSrcReviews__/cli/__init__.py' "$@"
}
