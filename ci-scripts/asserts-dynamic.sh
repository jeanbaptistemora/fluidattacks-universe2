#!/usr/bin/env sh

# Do not run asserts mock checks on dev
if [ "$CI_COMMIT_REF_NAME" != 'master' ]; then
  rm /exploits/*.mock.exp
fi

cp -a ./* /code/
/entrypoint.sh
