# shellcheck shell=bash

deploy \
  dev \
  development \
  "${CI_COMMIT_REF_NAME}"
