# shellcheck shell=bash

function main {
      find "${envAirs}" -type f -name cover.png > files \
  &&  while read -r path
      do
        if ! test "$(identify -format "%wx%h" "${path}")" = '900x600'
        then
          abort "[ERROR] ${path} must be 900x600 pixels"
        fi
      done < files \
  &&  touch "${out}"
}

main "${@}"
