#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell --cores 0
#!   nix-shell --max-jobs auto
#!   nix-shell shell.nix
#  shellcheck shell=bash

. "${stdenv}/setup"
. "${genericShellOptions}"

#
# CLI flags / Gitlab CI jobs
#

function cli {
  local command

  # Export vars to the current environment:
  #   --env var1_name var1_value --env var2_name var2_value ...
  while true
  do
    if test "${1:-}" = '--env'
    then
      shift 1
      echo "/nix/env: setting environment var ${1:-}"
      export "${1:-}"="${2:-}"
      shift 2 || (
        echo 'Expected: --env var_name var_value' && exit 1
      )
    else
      break
    fi
  done

  # Dispatch a group of commands based on the provided arguments
  # '--xxx' will call 'xxx' function
  # '-c' will execute a single command and exit
  case "${1:-}" in
    '-c') {
        eval "${2:-}";
        return 0;
      };;
    *) {
        # Remove initial dashes: '--aaa-bbb' -> 'aaa-bbb'
        command="${1#*--}"
        shift 1
        # Replace dash with underscore: 'aaa-bbb' -> 'aaa_bbb'
        "${command//-/_}" "${@}"
        return 0;
      };;
  esac
}

cli "${@}"
