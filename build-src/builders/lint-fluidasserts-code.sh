# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcDotGitShallow}" root/src/repo/.git
cp -r --no-preserve=mode,ownership \
  "${srcDotOvercommit}" root/src/repo/.overcommit.yml
cp -r --no-preserve=mode,ownership \
  "${srcDotPreCommitConfig}" root/src/repo/.pre-commit-config.yaml
cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts

cp -r --no-preserve=mode,ownership \
  "${pyPkgFluidasserts}"/* root/python
cp -r --no-preserve=mode,ownership \
  "${pyPkgGroupLint}"/* root/python

chmod +x root/python/site-packages/bin/flake8
chmod +x root/python/site-packages/bin/mypy
chmod +x root/python/site-packages/bin/pep257
chmod +x root/python/site-packages/bin/prospector
chmod +x root/python/site-packages/bin/pycodestyle
chmod +x root/python/site-packages/bin/pydocstyle
chmod +x root/python/site-packages/bin/pyflakes
chmod +x root/python/site-packages/bin/pylint
chmod +x root/python/site-packages/bin/yamllint

PATH="${PWD}/root/python/site-packages/bin:${PATH}"
PYTHONPATH="${PYTHONPATH}:${PWD}/root/python/site-packages"

pushd root/src/repo

git add .
overcommit -s
overcommit -s pre-commit
overcommit -r

prospector \
    --full-pep8 \
    --without-tool pep257 \
    --with-tool pyroma \
    --strictness veryhigh \
    --output-format text \
    --pylint-config-file="${srcBuildSrcConfigPylintrc}" \
  fluidasserts/

echo "${name} succeeded!" > "${out}"
