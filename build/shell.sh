#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --cores 0
#!   nix-shell --keep CI_COMMIT_REF_NAME
#!   nix-shell --keep CI_JOB_ID
#!   nix-shell --keep CI_PROJECT_DIR
#!   nix-shell --keep CI_REGISTRY_USER
#!   nix-shell --keep CI_REGISTRY_PASSWORD
#!   nix-shell --keep GITLAB_TOKEN
#!   nix-shell --max-jobs auto
#!   nix-shell --option restrict-eval false
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell --show-trace
#!   nix-shell shell.nix
#  shellcheck shell=bash

source "${srcIncludeGenericShellOptions}"
source "${srcIncludeCli}"

cli "${@}"
