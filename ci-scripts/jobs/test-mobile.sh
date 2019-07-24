#!/usr/bin/env bash

test_mobile() {

  # Runs linters and unit tests on mobile

  cp -a /usr/src/app/node_modules mobile/
  cd mobile/ || return 1
  npm install

  # Linters
  npx tslint -p tsconfig.json -t codeFrame

  # Unit tests
  npx tsc -p tsconfig.json
  npx jest

  cd "$CI_PROJECT_DIR" || return 1
}

test_mobile
