#!/usr/bin/env bash

ERRORS=0
CHANGED=$(git diff --name-only HEAD origin/master)

function error {
  echo -e "\\e[1;31!!m${1}\\e[0m" >&2
  ERRORS=1  # to activate set to 1. 0 test mode
}

echo "${CHANGED:-(None)}"
echo -e "\\e[1;31m^--Files modified vs origin/master.\\e[0m\\n"

# Run precommit on changed files
export PATH=$PATH:/usr/local/go/bin
if ! echo "$CHANGED" | xargs pre-commit run -v --files; then
  error "Precommit failed"
  echo "See (future:webpage docs|now:https://pre-commit.com/)"
else
  echo "Precommit passed, continue checks..."
fi

exit ${ERRORS}
# $ shellcheck check-changed.sh
# $
