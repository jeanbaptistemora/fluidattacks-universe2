#!/usr/bin/env bash

: "${1?"Extract text from asciidoc file. Usage: $0 file"}"

(pcregrep -M -v -e '^\[(source|"graphviz"|"plantuml").*\n^----((.|\n)*?)^----' | pcregrep -M -v -e '^----((.|\n)*?)^----' | sed -e 's/link:.*\[//g'| sed -e 's/<<.*>>//g' | sed -e 's/\[\[.*\]]//g' | pcregrep -v '^[+:]') < "$1"
