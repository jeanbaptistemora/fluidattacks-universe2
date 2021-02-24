# shellcheck shell=bash

function skims {
      export HOME="${HOME_IMPURE}" \
  &&  python3.8 '__envSrcSkimsSkims__/cli/__init__.py' "$@"
}
