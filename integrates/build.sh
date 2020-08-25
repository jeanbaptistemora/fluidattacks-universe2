#! /usr/bin/env bash

function boostrap_and_run {
  # Found myself doing it very often, let's wrap it!

      pushd .. \
    &&  ./build.sh "${@}" \
  &&  popd \
  ||  return 1
}

boostrap_and_run "${@}"
