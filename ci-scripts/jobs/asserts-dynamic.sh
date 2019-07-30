#!/usr/bin/env sh

asserts_dynamic() {

  # Runs Asserts dynamic checks on repo

  set -e

  export BRANCH
  export FA_STRICT
  export ORG
  export PASS
  export USER

  BRANCH=$CI_COMMIT_REF_NAME
  FA_STRICT='true'
  ORG='fluid'
  PASS=$INTEGRATES_JFROG_PASS
  USER=$INTEGRATES_JFROG_USER

  # Do not run asserts mock checks on dev
  if [ "$CI_COMMIT_REF_NAME" != 'master' ]; then
    rm /exploits/*.mock.exp
  fi

  cp -a ./* /code/
  /entrypoint.sh
}

asserts_dynamic
