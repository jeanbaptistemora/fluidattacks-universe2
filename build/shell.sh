#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --cores 0
#!   nix-shell --keep CI_REGISTRY_USER
#!   nix-shell --keep CI_REGISTRY_PASSWORD
#!   nix-shell --max-jobs auto
#!   nix-shell --option restrict-eval false
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell --show-trace
#!   nix-shell shell.nix
#  shellcheck shell=bash

source "${srcIncludeCli}"

cli "${@}"
