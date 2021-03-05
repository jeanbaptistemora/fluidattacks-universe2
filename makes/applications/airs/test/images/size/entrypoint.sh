# shellcheck shell=bash

function optimize_png {
  if optipng -o7 -simulate -zm1-9 "${path}" 2>&1 \
      | grep --fixed-strings 'already optimized'
  then
    echo "[INFO] Image is optimized: ${path}"
  else
    abort "[ERROR] Image is not optimized with $ optipng -o7 -zm1-9 ${path}"
  fi
}

function main {
  get_touched_files_last_commit \
    | (grep -P '\.png$' || cat) \
    | while read -r path
      do
            optimize_png "${path}" \
        ||  return 1
      done
}

main "${@}"
