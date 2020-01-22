# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

cp -r --no-preserve=mode,ownership \
  "${srcBuildSh}" root/src/repo/build.sh
cp -r --no-preserve=mode,ownership \
  "${srcBuildSrc}" root/src/repo/build-src
cp -r --no-preserve=mode,ownership \
  "${srcEnvrcPublic}" root/src/repo/.envrc.public

pushd root/src/repo

# Lint build code
path_to_check='build-src'
echo "Verifying shell code in: ${path_to_check}"
find "${path_to_check}" -name '*.sh' \
  -exec shellcheck --exclude=SC1090,SC2154,SC2164 -x {} +

# Lint top level files
shellcheck -x --exclude=SC2015 ./build.sh

echo "${name} succeeded!" > "${out}"
