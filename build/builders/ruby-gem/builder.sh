# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

pushd root/gems || exit 1

gem install \
  --install-dir ./ \
  --no-document "${requirement}"

mkdir "${out}"
mv ./* "${out}"
