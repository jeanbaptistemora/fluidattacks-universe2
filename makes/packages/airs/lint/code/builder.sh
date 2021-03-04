# shellcheck shell=bash

function main {
      copy2 "${envAirsNewFront}" new-front \
  &&  copy2 "${envLintConfig}/.eslintrc.json" new-front/.eslintrc.json \
  &&  pushd new-front \
    &&  copy2 "${envAirsNpm}/node_modules" 'node_modules' \
    &&  HOME=. ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    &&  HOME=. ./node_modules/.bin/eslint . --ext .js,.ts,.tsx --format codeframe \
  &&  popd \
  &&  touch "${out}" \
  ||  return 1
}

main "${@}"
