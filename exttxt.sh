#!/usr/bin/env bash

# This script removes code and diagram blocks, as well as other Asciidoc macros
# in order to extract only the text of the document and have an accurate
# measure of word count and LIX readability index.

: "${1?"Extract text from asciidoc file. Usage: $0 file"}"

(pcregrep -M -v -e '^\[(source|"graphviz"|"plantuml").*\n^----((.|\n)*?)^----' \
  -e '^(----|\+\+\+\+|\.\.\.\.)((.|\n)*?)^(----|\+\+\+\+|\.\.\.\.)' \
  | pcregrep -v -e '^\.[a-zA-Z0-9].*' \
  | sed -e 's/link:.*\[//g' \
    -e 's/<<.*>>//g' \
    -e 's/\[\[.*\]]//g' \
    -e 's/image:*.*\[.*\]//g' \
    -e 's/tooltip:.*\[//g' \
    -e 's/\[button\]\#//g' \
    -e 's/\[inner\]\#//g' \
  | pcregrep -v '^[+:]') < "$1"
