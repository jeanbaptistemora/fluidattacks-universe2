# shellcheck shell=bash

function main {
  local ruby_gems=(
    __envToolsConcurrentRuby__
  )

  for ruby_gem in "${ruby_gems[@]}"; do
    export GEM_PATH="${ruby_gem}:${GEM_PATH:-}" \
      && export PATH="${ruby_gem}/bin:${PATH:-}" \
      || return 1
  done
}

main "${@}"
