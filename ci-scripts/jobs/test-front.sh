#!/usr/bin/env bash

test_front() {

  # Runs linters and unit tests on front

  set -e

  cp -a /npm-deps/front/node_modules front/
  cd front/ || return 1
  npm install --unsafe-perm

  npm set audit-level high
  npm config set audit-level high
  npm audit

  # Linters
  npx tslint -p tsconfig.json -t codeFrame

  # Unit tests
  npx tsc -p tsconfig.json --noEmit
  npx tcm src/ --silent
  set -o pipefail
  npx jest --detectOpenHandles
  mv coverage/lcov.info coverage.lcov
  rm -r coverage

  cd "$CI_PROJECT_DIR" || return 1
}

test_front
