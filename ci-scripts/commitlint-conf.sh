#!/usr/bin/env bash

#This scripts download commitlint's configuration files

COMMITLINT_RULES_NAME='commitlint.config.js'
COMMITLINT_PARSER_NAME='parser-preset.js'
COMMITLINT_BASE_URL='https://gitlab.com/fluidattacks/default/raw/master/commitlint-configs/others'
COMMITLINT_RULES_URL="$COMMITLINT_BASE_URL/$COMMITLINT_RULES_NAME"
COMMITLINT_PARSER_URL="$COMMITLINT_BASE_URL/$COMMITLINT_PARSER_NAME"

curl $COMMITLINT_RULES_URL > $COMMITLINT_RULES_NAME 2> /dev/null
curl $COMMITLINT_PARSER_URL > $COMMITLINT_PARSER_NAME 2> /dev/null
