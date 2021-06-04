# shellcheck shell=bash

function lint_markdown {
  local path="${1}"

  mdl --style '__envStyle__' "${path}"
}
