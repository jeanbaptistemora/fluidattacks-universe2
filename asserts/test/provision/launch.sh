#! /usr/bin/env bash

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

module="${1}"
context="${2}"
exposed_port="${3}"

tag_name="registry.gitlab.com/fluidattacks/product/asserts/${module}:${context}"
context_path="./test/provision/${module}/${context}/"

{
  test "${module}" && test "${context}" && test "${exposed_port}"
} || {
  echo "Use example: ${0} [module] [context] [port]"
  echo "Use example: ${0} postgresql hard 5432"
  echo "Use example: ${0} postgresql weak 5432"
  echo "Use example: ${0} ssl hard 443"
  exit 1
}

docker build --tag "${tag_name}" "${context_path}" \
  && docker run \
    --rm \
    --tty \
    --interactive \
    --publish "${exposed_port}:${exposed_port}" \
    --name "${module}_${context}" \
    "${tag_name}"
