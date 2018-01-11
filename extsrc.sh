#!/usr/bin/env bash

: "${1?"Extract source code from asciidoc file. Usage: $0 file"}"

pcregrep -M -o1 '^\[source.*\n^----((.|\n)*?)^----' < "$1"
