#!/usr/bin/env bash

# This script aims to normalize content across the website, regarding the
# redaction of articles and pages, and the optimization of the images.

ERRORS=0

PREV_COMMIT=$(curl --header "Private-Token:$DOCKER_PASSWD" \
"https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/repository/commits/master" \
| pcregrep -o '(?<="id":")[^,"]*')
export PREV_COMMIT

# Check files that have been added or modified, respect to the master branch
CHANGED=$(git diff --name-status "$PREV_COMMIT"  "$CI_COMMIT_SHA" \
  | pcregrep -o '(?<=(M|A)\t).*')

# Function that displays an error message in red.
function error {
  echo -e "\\e[1;31m^--${1}\\e[0m\\n" >&2
  ERRORS=0  # to activate set to 1. 0 test mode
}

echo "${CHANGED:-(None)}"
echo -e "\\e[1;31m^--Files modified in this merge request.\\e[0m\\n"

# Check that the LIX remains under 50
if echo "$CHANGED" | pcregrep '^content.*adoc$' \
| xargs -r -n 1 ./lix.sh \
| pcregrep '^[5-9]\d\s'; then
  error "LIX readability index out of range. Should be <50.";
fi

# Check that documents in Defends have between 400 and 800 words
if echo "$CHANGED" | pcregrep '^content/defends.*adoc$' \
| xargs -r -n 1 ./words.sh \
| pcregrep -v '^([4-8]\d\d\s)'; then
  error "Number of words in KB text out of range. Should be 400>=words<800.";
fi

# Check that blog articles have between 800 and 1600 words
if echo "$CHANGED" | pcregrep '^content/blog.*adoc$' \
| xargs -r -n 1 ./words.sh \
| pcregrep -v '^([8-9]\d\d|^1[0-5]\d\d)\s'; then
  error "Number of words in posts out of range. Should be 800>=words<1600.";
fi

# Check that pages have between 400 and 1600 words
if echo "$CHANGED" | pcregrep '^content/pages.*adoc$' \
| xargs -r -n 1 ./words.sh \
| pcregrep -v '^([4-9]\d\d|^1[0-5]\d\d)\s'; then
  error "Number of words in pages out of range. Should be 400>=words<1600.";
fi

# Check that every PNG files has been optimized in filesize
if echo "$CHANGED" | pcregrep '\.png$'; then
  if ! echo "$CHANGED" | pcregrep '\.png$'\
  | xargs -r -n 1 optipng |& pcregrep 'optimized'; then
    error "Some PNG files are not optimized. Run the CLI tool \"optipng\" \
    to optimize them or go to http://compresspng.com/."
    ERRORS=1;
  fi;
fi

exit ${ERRORS}
