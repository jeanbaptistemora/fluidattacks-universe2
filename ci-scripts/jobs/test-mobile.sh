#!/usr/bin/env bash

test_mobile() {

  # Runs linters and unit tests on mobile

  set -e

  cp -a /usr/src/app/node_modules mobile/
  cd mobile/ || return 1
  # Linters
  npm run lint

  # Unit tests
  npm test

  cd "$CI_PROJECT_DIR" || return 1
}

test_mobile
