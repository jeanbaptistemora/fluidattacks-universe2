# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

pushd root/nodejs || exit 1

HOME=. npm install --unsafe-perm "${requirement}"

mkdir "${out}"
mv ./* "${out}"
