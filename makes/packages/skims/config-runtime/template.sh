# shellcheck shell=bash

export HOME="${HOME_IMPURE:-${HOME}}"
export PYTHONHASHSEED=0

function skims {
  python3.8 '__envSrcSkimsSkims__/cli/__init__.py' "$@"
}
