#!/usr/bin/env bash

test_front() {

  # Runs linters and unit tests on front

  set -e

  cp -a /npm-deps/front/node_modules front/
  cd front/ || return 1
  npm install --unsafe-perm

  npm run audit

  # Linters
  npm run lint

  # Unit tests
  set -o pipefail
  npm test
  mv coverage/lcov.info coverage.lcov
  rm -r coverage

  cd "$CI_PROJECT_DIR" || return 1
}

test_front
