# shellcheck shell=bash

function forces {
  python3.8 '__argSrcForces__/forces/cli/__init__.py' "$@"
}
