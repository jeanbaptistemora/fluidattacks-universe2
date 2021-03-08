# shellcheck shell=bash

function forces {
  python3.8 '__envSrcForces__/forces/cli/__init__.py' "$@"
}
