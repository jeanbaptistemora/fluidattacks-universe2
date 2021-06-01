# shellcheck shell=bash

function main {
  local args_black=(
    --config '__envSettingsBlack__'
  )
  local args_isort=(
    --settings-path '__envSettingsIsort__'
  )
  local paths_black=__envTargetsBlack__
  local paths_isort=__envTargetsIsort__

      if test -n "${CI:-}"
      then
            args_black+=( --diff --check --color ) \
        &&  args_isort+=( --diff --check --color )
      fi \
  &&  for path in "${paths_black[@]}"
      do
        black "${args_black[@]}" "${path}"
      done \
  &&  for path in "${paths_isort[@]}"
      do
        isort "${args_isort[@]}" "${path}"
      done
}

main "${@}"
