# shellcheck shell=bash

function main {
  for kind in applications packages
  do
        echo "[INFO] Generating ${kind}" \
    &&  find "__envRoot__/makes/${kind}" -type f -name default.nix -exec dirname {} + \
          | sed "s|__envRoot__/makes/${kind}/||g" \
          | sort \
          > "makes/attrs/${kind}.lst" \
    ||  return 1
  done
}

main "${@}"
