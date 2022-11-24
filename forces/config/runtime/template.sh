# shellcheck shell=bash

function forces {
  python3.10 '__argSrcForces__/forces/cli/__init__.py' "$@"
}
