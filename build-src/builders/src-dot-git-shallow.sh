# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cd root/src/repo

git init
git config user.name "nixatfluid"
git config user.email "nix@fluidattacks.com"
git commit --allow-empty -m "$(cat "${srcGitLastCommitMsg}")"

mkdir "${out}"
mv .git/* "${out}"
