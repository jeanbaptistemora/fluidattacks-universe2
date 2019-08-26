#! /usr/bin/env bash

context="${1}"
tag_name="registry.gitlab.com/fluidattacks/asserts/mocks/postgresql:${context}"
context_path="./test/provision/postgresql/${context}/"

test "${context}" || {
  echo "Use: ${0} hard/weak";
  exit 1;
}

docker build --tag "${tag_name}" "${context_path}" \
&& docker run \
    --rm \
    --tty \
    --interactive  \
    --publish 5432:5432 \
    --name postgresql \
  "${tag_name}"
