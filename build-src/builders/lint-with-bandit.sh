# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts

pushd root/src/repo

bandit -ii -s B501,B601,B402,B105,B321,B102,B107,B307 -r fluidasserts

echo "${name} succeeded!" > "${out}"
