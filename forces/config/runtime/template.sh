# shellcheck shell=bash

function forces {
  python3.11 '__argSrcForces__/forces/cli/__init__.py' "$@"
}
