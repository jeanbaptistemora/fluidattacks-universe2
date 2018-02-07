#!/usr/bin/env bash

: "${1?"Extract text from asciidoc file. Usage: $0 file"}"

(pcregrep -M -v '^\[source.*\n^----((.|\n)*?)^----' | sed -e 's/link:.*\[//g'| sed -e 's/<<.*>>//g' | sed -e 's/\[\[.*\]]//g' | pcregrep -v '^[+:]') < "$1"
