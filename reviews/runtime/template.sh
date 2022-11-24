# shellcheck shell=bash

function reviews {
  python '__argSrcReviews__/cli/__init__.py' "$@"
}
