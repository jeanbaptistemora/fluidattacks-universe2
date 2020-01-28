# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

mkdir root/src/repo/build-src
mkdir root/src/repo/build-src/config

cp -r --no-preserve=mode,ownership \
  "${srcBuildSh}" root/src/repo/build.sh
cp -r --no-preserve=mode,ownership \
  "${srcBuildSrc}" root/src/repo/build-src
cp -r --no-preserve=mode,ownership \
  "${srcBuildSrcConfigReadmeRst}" root/src/repo/build-src/config/README.rst
cp -r --no-preserve=mode,ownership \
  "${srcBuildSrcScripts}" root/src/repo/build-src/scripts
cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts
cp -r --no-preserve=mode,ownership \
  "${srcManifestIn}" root/src/repo/MANIFEST.in
cp -r --no-preserve=mode,ownership \
  "${srcSetupPy}" root/src/repo/setup.py
cp -r --no-preserve=mode,ownership \
  "${srcTest}" root/src/repo/test

cp -r --no-preserve=mode,ownership \
  "${fluidassertsDependenciesCache}"/* root/python

pushd root/src/repo

# Patch the version to make it static
version=$(python3 ./build-src/scripts/get_version.py)
echo "Version: ${version}"
sed -i "s/_get_version(),/'${version}',/g" setup.py

# Source distribution
#   https://www.python.org/dev/peps/pep-0517/#source-distributions
#   * They will be gzipped tar archives, with the .tar.gz extension
python3 setup.py sdist --formats=gztar

# Binary distribution
#   https://packaging.python.org/specifications/distribution-formats/#binary-distribution-format
#   The binary distribution format (wheel) is defined in PEP 427.
#   * A wheel is a ZIP-format archive with a specially formatted file name and the .whl extension.
python3 setup.py bdist_wheel

ls -1 dist/

mv dist "${out}"
