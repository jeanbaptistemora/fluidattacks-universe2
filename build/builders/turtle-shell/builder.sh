# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

export TURTLE_ANDROID_DEPENDENCIES_DIR=root/turtle/android/
export TURTLE_WORKING_DIR_PATH=root/turtle/shell/

npx turtle-cli@0.14.11 \
  setup:android \
  --sdk-version "${sdkVersion}" \
&& yes | root/turtle/android/sdk/tools/bin/sdkmanager --licenses

mkdir "${out}"
mv root/turtle/* "${out}"
