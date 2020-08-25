#! /usr/bin/env bash

function bootstrap_and_run {
  # Found myself doing it very often, let's wrap it!

      pushd .. \
    &&  ./build.sh "${@}" \
  &&  popd \
  ||  return 1
}

bootstrap_and_run "${@}"
