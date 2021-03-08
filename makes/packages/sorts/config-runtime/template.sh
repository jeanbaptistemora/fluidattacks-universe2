# shellcheck shell=bash

function sorts {
  python3.8 '__envSrcSortsSorts__/cli/__init__.py' "$@"
}
