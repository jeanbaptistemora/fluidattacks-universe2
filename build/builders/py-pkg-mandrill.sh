# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

pip3 install \
    --cache-dir root/python/cache-dir \
    --target    root/python/site-packages \
    --upgrade \
  'mandrill-really-maintained==1.2.4'

mkdir "${out}"
mv root/python/* "${out}"
