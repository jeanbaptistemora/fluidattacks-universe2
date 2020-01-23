# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

pip3 install \
    --cache-dir root/python/cache-dir \
    --target    root/python/site-packages \
    --upgrade \
  'git-fame==1.10.1'

mkdir "${out}"
mv root/python/* "${out}"
