# shellcheck shell=bash

function install_fontawesome_pro {
  local deps=(
    @fortawesome/fontawesome-pro@5.15.3
    @fortawesome/pro-duotone-svg-icons@5.15.3
    @fortawesome/pro-light-svg-icons@5.15.3
    @fortawesome/pro-regular-svg-icons@5.15.3
    @fortawesome/pro-solid-svg-icons@5.15.3
  )

  npm install "${deps[@]}"
}
