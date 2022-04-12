# shellcheck shell=bash

function install_scripts {
  : \
    && rm -rf node_modules/sharp \
    && npm install --ignore-scripts=false
}
