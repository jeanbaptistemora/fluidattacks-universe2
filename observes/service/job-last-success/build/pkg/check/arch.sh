# shellcheck shell=bash

echo "Executing architecture check phase" \
  && lint-imports --config "arch.cfg" \
  && echo "Finished architecture check phase"
