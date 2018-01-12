#!/usr/bin/env bash

: "${1?"LIX index of the text. Usage: $0 file"}"

echo -e "$(./exttxt.sh $1 | style | pcregrep -o1 'Lix: (\d\d)' || echo 0)\t$1"
