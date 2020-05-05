# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

gem install \
  --install-dir root/gems \
  --no-document "${requirement}"

mkdir "${out}"
mv root/gems/* "${out}"
