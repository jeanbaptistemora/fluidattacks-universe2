# shellcheck shell=bash

if test -n "${HOME_IMPURE:-}"; then
  export HOME="${HOME_IMPURE}"
fi
export PYTHONHASHSEED=0

function skims {
  python3.8 '__argSrcSkimsSkims__/cli/__init__.py' "$@"
}
