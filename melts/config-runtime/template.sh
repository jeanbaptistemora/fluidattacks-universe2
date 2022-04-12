# shellcheck shell=bash

function melts_setup_runtime {
  # Leave melts use the host's home in order to allow credentials to live
  # many hours
  export HOME
  export HOME_IMPURE

  if test -n "${HOME_IMPURE:-}"; then
    HOME="${HOME_IMPURE}"
  fi
}

function melts {
  python3.8 '__argSrcMelts__/toolbox/cli/__init__.py' "$@"
}

melts_setup_runtime
