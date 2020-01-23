# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts

cp -r --no-preserve=mode,ownership \
  "${pyPkgFluidasserts}"/* root/python
cp -r --no-preserve=mode,ownership \
  "${pyPkgGroupLinters}"/* root/python

chmod +x root/python/site-packages/bin/prospector

PATH="${PWD}/root/python/site-packages/bin:${PATH}"
PYTHONPATH="${PYTHONPATH}:${PWD}/root/python/site-packages"

pushd root/src/repo

prospector \
    --full-pep8 \
    --without-tool pep257 \
    --with-tool pyroma \
    --strictness veryhigh \
    --output-format text \
    --pylint-config-file="${srcBuildSrcConfigPylintrc}" \
  fluidasserts/

echo "${name} succeeded!" > "${out}"
