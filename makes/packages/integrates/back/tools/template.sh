# shellcheck shell=bash

function main {
  local node_pkgs=(
    __envToolsSecureSpreadsheet__
  )
  local ruby_gems=(
    __envToolsAsciidoctor__
    __envToolsAsciidoctorPdf__
    __envToolsConcurrentRuby__
  )

      for node_pkg in "${node_pkgs[@]}"
      do
            export NODE_PATH="${node_pkg}/node_modules:${NODE_PATH:-}" \
        &&  export PATH="${node_pkg}/node_modules/.bin:${PATH:-}" \
        ||  return 1
      done \
  &&  for ruby_gem in "${ruby_gems[@]}"
      do
            export GEM_PATH="${ruby_gem}:${GEM_PATH:-}" \
        &&  export PATH="${ruby_gem}/bin:${PATH:-}" \
        ||  return 1
      done
}

main "${@}"
