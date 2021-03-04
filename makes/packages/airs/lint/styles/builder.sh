# shellcheck shell=bash

function main {
      copy2 "${envAirsNewFront}" new-front \
  &&  pushd new-front \
    &&  copy2 "${envAirsNpm}/node_modules" 'node_modules' \
    &&  HOME=. ./node_modules/.bin/stylelint '**/*.scss' \
  &&  popd \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
