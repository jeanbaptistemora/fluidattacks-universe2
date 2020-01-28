# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

mkdir root/src/repo/conf

cp -r --no-preserve=mode,ownership \
  "${srcConfReadmeRst}" root/src/repo/conf/README.rst
cp -r --no-preserve=mode,ownership \
  "${srcBuildSh}" root/src/repo/build.sh
cp -r --no-preserve=mode,ownership \
  "${srcBuildSrc}" root/src/repo/build-src
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

# Source distribution in ALL formats
python3 setup.py \
    sdist \
  --quiet \
  --dist-dir 'dist' \
  --formats=bztar,gztar,xztar,ztar,tar,zip

# Binary distribution
python3 setup.py \
    bdist \
  --dist-dir 'dist' \
  --formats=bztar,gztar,xztar,ztar,tar,zip

ls -1 dist/

mv dist "${out}"
