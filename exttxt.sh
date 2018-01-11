#!/usr/bin/env bash

: "${1?"Extract text from asciidoc file. Usage: $0 file"}"

(pcregrep -M -v '^\[source.*\n^----((.|\n)*?)^----' | pcregrep -v '^[+:]') < "$1"
