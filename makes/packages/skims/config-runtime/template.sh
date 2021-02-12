# shellcheck shell=bash

function skims {
  python3.8 '__envSrcSkimsSkims__/cli/__init__.py' "$@"
}
