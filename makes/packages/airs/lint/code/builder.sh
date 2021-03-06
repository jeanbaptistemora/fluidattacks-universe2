# shellcheck shell=bash

function main {
      copy "${envAirsNewFront}" new-front \
  &&  copy "${envLintConfig}/.eslintrc.json" new-front/.eslintrc.json \
  &&  pushd new-front \
    &&  copy "${envAirsNpm}/node_modules" 'node_modules' \
    &&  HOME=. ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    &&  HOME=. ./node_modules/.bin/eslint . --ext .js,.ts,.tsx --format codeframe \
  &&  popd \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
