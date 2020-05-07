# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

export HOME="${PWD}/root/"
export ANDROID_SDK_HOME=${HOME}

npx turtle-cli@0.14.11 \
  setup:android \
  --sdk-version "${sdkVersion}"

mkdir "${out}"
mv root/.turtle/* "${out}"
