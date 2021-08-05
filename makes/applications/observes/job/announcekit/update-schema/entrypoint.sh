# shellcheck shell=bash

alias tap-announcekit="observes-bin-tap-announcekit"

tap-announcekit update-schema \
  --out "./observes/singer/tap_announcekit/tap_announcekit/api/gql_schema.py"
