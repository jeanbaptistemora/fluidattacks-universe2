#!/usr/bin/env bash

test_mobile() {

  # Runs linters and unit tests on mobile

  cp -a /usr/src/app/node_modules mobile/
  cd mobile/ || exit 1
  npm install

  # Linters
  tslint -p tsconfig.json -t codeFrame

  # Unit tests
  tsc -p tsconfig.json
  jest

  cd "$CI_PROJECT_DIR" || return 1
}

test_mobile
