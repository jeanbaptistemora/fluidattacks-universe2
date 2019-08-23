#! /usr/bin/env bash

context="${1}"

test "${context}" || {
  echo "Use: ${0} hard/weak";
  exit 1;
}

docker build \
    --tag postgresql \
  "./test/provision/postgresql/${context}/" \
&& docker run \
    --rm \
    --tty \
    --interactive  \
    --publish 5432:5432 \
    --name postgresql \
  postgresql
