# shellcheck shell=bash

echo "Executing type check phase" \
  && mypy --version \
  && mypy . \
  && echo "Finished type check phase"
