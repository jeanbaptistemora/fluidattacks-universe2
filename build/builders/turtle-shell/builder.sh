# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

export TURTLE_ANDROID_DEPENDENCIES_DIR=root/turtle/android/
export TURTLE_WORKING_DIR_PATH=root/turtle/shell/

HOME=. npx turtle-cli@0.14.11 \
  setup:android \
  --sdk-version "${sdkVersion}"

mkdir "${out}"
mv root/turtle/* "${out}"
