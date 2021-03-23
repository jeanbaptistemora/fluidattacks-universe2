# shellcheck shell=bash

function main {
      copy "${envAirsNewFront}" new-front \
  &&  pushd new-front \
    &&  copy "${envAirsNpm}/node_modules" 'node_modules' \
    &&  ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    &&  lint_typescript "$(pwd)" "$(pwd)" \
  &&  popd \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
