#!/usr/bin/env bash

# This script removes code and diagram blocks, as well as other Asciidoc macros
# in order to extract only the text of the document and have an accurate
# measure of word count and LIX readability index.

: "${1?"Extract text from asciidoc file. Usage: $0 file"}"

(pcregrep -M -v -e '^\[(source|"graphviz"|"plantuml").*\n^----((.|\n)*?)^----' | pcregrep -M -v -e '^----((.|\n)*?)^----' | sed -e 's/link:.*\[//g'| sed -e 's/<<.*>>//g' | sed -e 's/\[\[.*\]]//g' | pcregrep -v '^[+:]') < "$1"
