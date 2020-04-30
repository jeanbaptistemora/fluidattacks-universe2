#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --cores 0
#!   nix-shell --keep AWS_ACCESS_KEY_ID
#!   nix-shell --keep AWS_DEFAULT_REGION
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY
#!   nix-shell --keep BREAK_BUILD_ID
#!   nix-shell --keep BREAK_BUILD_SECRET
#!   nix-shell --keep CI
#!   nix-shell --keep CI_JOB_ID
#!   nix-shell --keep NIX_PATH
#!   nix-shell --keep CI_COMMIT_REF_NAME
#!   nix-shell --keep CI_COMMIT_SHA
#!   nix-shell --keep CI_PIPELINE_SOURCE
#!   nix-shell --keep CI_PROJECT_DIR
#!   nix-shell --keep CI_REGISTRY_USER
#!   nix-shell --keep CI_REGISTRY_PASSWORD
#!   nix-shell --keep GITLAB_API_TOKEN
#!   nix-shell --keep GITLAB_CI
#!   nix-shell --max-jobs auto
#!   nix-shell --option restrict-eval false
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell --show-trace
#!   nix-shell shell.nix
#  shellcheck shell=bash

source "${srcIncludeCli}"
source "${srcIncludeGenericShellOptions}"

cli "${@}"
