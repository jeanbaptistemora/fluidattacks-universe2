# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts
cp -r --no-preserve=mode,ownership \
  "${srcTest}" root/src/repo/test

cp -r --no-preserve=mode,ownership \
  "${pyPkgFluidassertsBasic}/"* root/python

chmod +x root/python/site-packages/bin/asserts

PATH="${PWD}/root/python/site-packages/bin:${PATH}"
PYTHONPATH="${PYTHONPATH}:${PWD}/root/python/site-packages"

pushd root/src/repo

export FA_NOTRACK='true'
export FA_STRICT='false'
asserts --kiss --multiprocessing --show-method-stats --cloudformation test

echo "${name} succeeded!" > "${out}"
