#!/usr/bin/env bash

ERRORS=0

CHANGED=$(git diff HEAD~ --name-only)

function error {
  if [ ${?} -eq 0 ]; then
    echo -e "\e[1;31m^--${1}\e[0m\n" >&2
    ERRORS=0  # to activate set to 1. 0 test mode
  fi
}

echo "${CHANGED:-(None)}"
echo -e "\e[1;31m^--Files modified in this merge request.\e[0m\n"

echo "$CHANGED" | pcregrep '^content.*adoc$' \
  | xargs -r -n 1 ./lix.sh \
  | pcregrep '^[5-9]\d\s'
error "LIX readability index out of range. Should be <50."

echo "$CHANGED" | pcregrep '^content/kb.*adoc$' \
  | xargs -r -n 1 ./words.sh \
  | pcregrep -v '^([4-8]\d\d\s)'
error "Number of words in KB text out of range. Should be 400>=words<800."

echo "$CHANGED" | pcregrep '^content/blog.*adoc$' \
  | xargs -r -n 1 ./words.sh \
  | pcregrep -v '^([8-9]\d\d|^1[0-1]\d\d)\s'
error "Number of words in posts out of range. Should be 800>=words<1200."

echo "$CHANGED" | pcregrep '^content/pages.*adoc$' \
  | xargs -r -n 1 ./words.sh \
  | pcregrep -v '^([4-9]\d\d|^1[0-5]\d\d)\s'
error "Number of words in pages out of range. Should be 400>=words<1600."

exit ${ERRORS}
