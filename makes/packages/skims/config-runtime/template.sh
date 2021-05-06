# shellcheck shell=bash

function skims {
      export HOME="${HOME_IMPURE:-${HOME}}" \
  &&  python3.8 '__envSrcSkimsSkims__/cli/__init__.py' "$@"
}
