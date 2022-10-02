# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

case "${1:-}" in
  css) prettier --parser css ;;
  html) prettier --parser html ;;
  javascript) prettier --parser babel ;;
  json) jq -S ;;
  markdown) prettier --parser markdown ;;
  python)
    black --config __argSettingsBlack__ - \
      | isort --settings-path __argSettingsISort__ -
    ;;
  scss) prettier --parser scss ;;
  shellscript) shfmt -bn -ci -i 2 -s -sr - ;;
  terraform) terraform fmt - ;;
  toml)
    NODE_PATH="__argPrettierPluginToml__/lib/node_modules${NODE_PATH:+:}${NODE_PATH:-}" \
      prettier \
      --parser toml \
      --plugin prettier-plugin-toml
    ;;
  xml) prettier --parser html ;;
  yaml) prettier --parser yaml ;;
  *) critical "Unsupported language: ${1:-}." ;;
esac
