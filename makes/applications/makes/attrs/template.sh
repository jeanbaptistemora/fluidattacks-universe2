# shellcheck shell=bash

function main {
  for kind in applications packages
  do
        echo "[INFO] Generating ${kind}" \
    &&  __envFind__ "__envRoot__/makes/${kind}" -type f -name default.nix -exec dirname {} + \
          | __envSed__ "s|__envRoot__/makes/${kind}/||g" \
          | __envSed__ "s|/|.|g" \
          | sort \
          > "makes/attrs/${kind}.lst" \
    ||  return 1
  done
}

main "${@}"
