# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

mkdir root/src/repo/conf
mkdir root/src/repo/build
mkdir root/src/repo/build/config

cp -r --no-preserve=mode,ownership \
  "${srcBuildConfigReadmeRst}" root/src/repo/build/config/README.rst
cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts
cp -r --no-preserve=mode,ownership \
  "${srcManifestIn}" root/src/repo/MANIFEST.in
cp -r --no-preserve=mode,ownership \
  "${srcSetupPy}" root/src/repo/setup.py

cp -r --no-preserve=mode,ownership \
  "${fluidassertsDependenciesCache}"/* root/python

pip3 install \
    --cache-dir root/python/cache-dir \
    --disable-pip-version-check \
    --target    root/python/site-packages \
    --upgrade \
  root/src/repo

mkdir "${out}"
mv root/python/* "${out}"
