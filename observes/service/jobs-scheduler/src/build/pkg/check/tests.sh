# shellcheck shell=bash

echo "Executing test phase" \
  && pytest --version \
  && pytest . \
  && echo "Finished test phase"
