# shellcheck shell=bash

if test -n "${HOME_IMPURE:-}"; then
  export HOME="${HOME_IMPURE}"
fi
export PYTHONHASHSEED=0

function skims {
  aws_login_dev \
    && python '__argSrcSkimsSkims__/cli/__init__.py' "$@"
}
