# shellcheck shell=bash

function main {
  local args=(
    --config '__envSettingsBlack__'
  )
  local paths=__envTargets__

      if test -n "${CI:-}"
      then
        args+=( --diff --check --color )
      fi \
  &&  for path in "${paths[@]}"
      do
        black "${args[@]}" "${path}"
      done
}

main "${@}"
