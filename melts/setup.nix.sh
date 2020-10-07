# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

cp -r --no-preserve=mode,ownership \
  "${path}" "root/src/src"

# Remove some libraries that must be provided by nix
echo > root/src/src/requirements.txt

cp -r --no-preserve=mode,ownership \
    "${requirements}/cache-dir/"* 'root/python/cache-dir'
cp -r --no-preserve=mode,ownership \
    "${requirements}/site-packages/"* 'root/python/site-packages'
cp -r --no-preserve=mode,ownership \
    "${overridenPandas}/lib/python3.7/site-packages/"* 'root/python/site-packages'
cp -r --no-preserve=mode,ownership \
    "${pyPkgUtilities}/site-packages/"* 'root/python/site-packages'

pip3 install \
    --cache-dir root/python/cache-dir \
    --target    root/python/site-packages \
    --upgrade \
  "root/src/src"

cp -r --no-preserve=mode,ownership \
    "${requirements}/site-packages/bin/"* 'root/python/site-packages/bin'

if test -e "root/python/site-packages/bin"
then
  chmod +x "root/python/site-packages/bin/"*
fi

mkdir "${out}"
mv root/python/* "${out}"
