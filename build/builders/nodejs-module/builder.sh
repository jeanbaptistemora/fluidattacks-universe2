# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcGenericShellOptions}"
source "${srcGenericDirStructure}"

pushd root/nodejs || exit 1

HOME=. npm install --unsafe-perm "${requirement}"

mkdir "${out}"
mv ./* "${out}"
