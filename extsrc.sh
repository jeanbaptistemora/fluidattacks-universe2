#!/usr/bin/env bash

# This script removes the source codes from the .adoc files, so it does not
# affect the word count or the LIX readability index.

: "${1?"Extract source code from asciidoc file. Usage: $0 file"}"

pcregrep -M -o1 '^\[source.*\n^----((.|\n)*?)^----' < "$1"
