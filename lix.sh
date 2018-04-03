#!/usr/bin/env bash

# This script extracts the text of a document and evaluates its LIX readability
# index in order to assess the complexity of a document.
# This allows the setting of a LIX limit to keep documents in a certain
# complexity, depending of the target audience.

: "${1?"LIX index of the text. Usage: $0 file"}"

echo -e "$(./exttxt.sh "$1" | style | pcregrep -o1 'Lix: (\d\d)' || echo 0)\\t$1"
