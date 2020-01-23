# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcDeploy}" root/src/repo/deploy
cp -r --no-preserve=mode,ownership \
  "${srcDotGit}" root/src/repo/.git
cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts
cp -r --no-preserve=mode,ownership \
  "${srcSphinx}" root/src/repo/sphinx

cp -r --no-preserve=mode,ownership \
  "${pyPkgFluidasserts}/"* root/python
cp -r --no-preserve=mode,ownership \
  "${pyPkgGitFame}/"* root/python
cp -r --no-preserve=mode,ownership \
  "${pyPkgSphinx}/"* root/python

chmod +x root/src/repo/sphinx/gendoc.sh
chmod +x root/python/site-packages/bin/asserts
chmod +x root/python/site-packages/bin/git-fame
chmod +x root/python/site-packages/bin/sphinx-apidoc
chmod +x root/python/site-packages/bin/sphinx-build

PATH="${PWD}/root/python/site-packages/bin:${PATH}"
PYTHONPATH="${PYTHONPATH}:${PWD}/root/python/site-packages"

pushd root/src/repo

./sphinx/gendoc.sh

mv public "${out}"
