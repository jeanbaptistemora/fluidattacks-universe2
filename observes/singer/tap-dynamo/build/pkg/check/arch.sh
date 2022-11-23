# shellcheck shell=bash

echo "Executing architecture check phase" \
  && lint-imports --config "pkg.arch.cfg" \
  && echo "Finished architecture check phase"
