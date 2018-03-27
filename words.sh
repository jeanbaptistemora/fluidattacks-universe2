#!/usr/bin/env bash

: "${1?"Number of words on the text. Usage: $0 file"}"

echo -e "$(./exttxt.sh "$1" | style | pcregrep -o1 '(\d*) words,' || echo 0)\\t$1"
