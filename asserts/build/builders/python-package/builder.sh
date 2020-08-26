# shellcheck shell=bash

source "${stdenv}/setup"
source "${srcIncludeGenericShellOptions}"
source "${srcIncludeGenericDirStructure}"

pip3 install \
    --cache-dir root/python/cache-dir \
    --target    root/python/site-packages \
    --upgrade \
  "${requirement}"

if test -e "root/python/site-packages/bin"
then
  chmod +x "root/python/site-packages/bin/"*
fi

mkdir "${out}"
mv root/python/* "${out}"
