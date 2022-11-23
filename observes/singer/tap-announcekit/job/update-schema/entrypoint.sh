# shellcheck shell=bash

alias tap-announcekit="observes-singer-tap-announcekit-bin"

tap-announcekit update-schema \
  --out "./observes/singer/tap-announcekit/src/tap_announcekit/api/gql_schema.py"
