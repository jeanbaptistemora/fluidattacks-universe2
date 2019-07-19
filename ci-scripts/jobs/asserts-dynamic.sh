#!/usr/bin/env sh

asserts_dynamic() {
  # Runs Asserts dynamic checks on repo

  # Do not run asserts mock checks on dev
  if [ "$CI_COMMIT_REF_NAME" != 'master' ]; then
    rm /exploits/*.mock.exp
  fi

  cp -a ./* /code/
  /entrypoint.sh
}

asserts_dynamic
