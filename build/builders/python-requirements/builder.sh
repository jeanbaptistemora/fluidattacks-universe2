# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

cp -r --no-preserve=mode,ownership \
  "${path}" "root/src/${name}"

# Remove some libraries that must be provided by nix
sed -i -E 's/^(python-magic|matplotlib).*$//g' "root/src/${name}"
cat "root/src/${name}"

pip3 install \
    --cache-dir root/python/cache-dir \
    --target    root/python/site-packages \
    --upgrade \
    --requirement \
  "root/src/${name}"

if test -e "root/python/site-packages/bin"
then
  chmod +x "root/python/site-packages/bin/"*
fi

mkdir "${out}"
mv root/python/* "${out}"
