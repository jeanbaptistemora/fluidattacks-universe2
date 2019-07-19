#!/usr/bin/env bash

test_front() {

  # Runs linters and unit tests on front

  cp -a /root/front/node_modules front/
  cd front/ || exit 1
  npm install --unsafe-perm

  npm set audit-level high
  npm config set audit-level high
  npm audit

  # Linters
  tslint -p tsconfig.json -t codeFrame

  # Unit tests
  tsc -p tsconfig.json --noEmit
  npm run css
  set -e
  set -o pipefail
  jest --detectOpenHandles
  mv coverage/lcov.info coverage.lcov
  rm -r coverage

  cd $CI_PROJECT_DIR || exit1
}

test_front
