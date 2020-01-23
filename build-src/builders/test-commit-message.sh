# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcDotGitShallow}" root/src/repo/.git

cp -r --no-preserve=mode,ownership \
  "${nodePkgCommitlint}"/* root/src/repo

cd root/src/repo

echo 'Executing commitlint ...'
git log -1 --pretty=%B HEAD | HOME=. npx commitlint

echo "${name} succeeded!" > "${out}"
