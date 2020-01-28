#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell --cores 0
#!   nix-shell --max-jobs auto
#!   nix-shell --attr releaseToDockerHub
#!   nix-shell --keep DOCKER_HUB_PASS
#!   nix-shell --keep DOCKER_HUB_URL
#!   nix-shell --keep DOCKER_HUB_USER
#!   nix-shell ./build-src/main.nix
#  shellcheck shell=bash

source "${genericShellOptions}"

function login {
  docker login "${DOCKER_HUB_URL}" -u "${DOCKER_HUB_USER}" --password-stdin \
    < <(echo "${DOCKER_HUB_PASS}")
}

function build {
  local image_name="${1}"
  local target_name="${2}"

  docker build --tag "${image_name}" --target "${target_name}" .
  docker push "${image_name}"
}

login
build 'fluidattacks/asserts:light' 'light'
build 'fluidattacks/asserts'       'full'
