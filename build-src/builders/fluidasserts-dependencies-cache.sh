# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

mapfile -t dependencies < <(grep -oP "[a-zA-Z0-9_-]+==[^']*" "${srcSetupPy}")

for dependency in "${dependencies[@]}"
do
  pip3 install \
      --cache-dir root/python/cache-dir \
      --target    root/python/site-packages \
      --upgrade \
    "${dependency}" &
done

wait

mkdir "${out}"
mv root/python/* "${out}"
