# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

pip3 install \
    --cache-dir root/python/cache-dir \
    --target    root/python/site-packages \
    --upgrade \
  'sphinx==2.2.1' \
  'sphinx-rtd-theme==0.4.3' \
  'sphinx-autodoc-typehints==1.10.3'

mkdir "${out}"
mv root/python/* "${out}"
