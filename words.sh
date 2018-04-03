#!/usr/bin/env bash

# This script extracts the text from a document and counts the words in it.
# It allows the setting of limits to keep documents in a certain length
# that better suits the target audience.

: "${1?"Number of words on the text. Usage: $0 file"}"

echo -e "$(./exttxt.sh "$1" | style | pcregrep -o1 '(\d*) words,' || echo 0)\\t$1"
