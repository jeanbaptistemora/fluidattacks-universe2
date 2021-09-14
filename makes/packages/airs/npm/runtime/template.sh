# shellcheck shell=bash

function install_fontawesome_pro {
  local options="${1}"
  local deps=(
    @fortawesome/fontawesome-pro@5.15.3
    @fortawesome/pro-duotone-svg-icons@5.15.3
    @fortawesome/pro-light-svg-icons@5.15.3
    @fortawesome/pro-regular-svg-icons@5.15.3
    @fortawesome/pro-solid-svg-icons@5.15.3
  )

  npm install "${options}" "${deps[@]}"
}

function install_scripts {
  : \
    && rm -rf node_modules/sharp \
    && npm install --ignore-scripts=false
}
