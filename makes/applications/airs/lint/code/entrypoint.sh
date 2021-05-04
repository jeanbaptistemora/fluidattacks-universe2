# shellcheck shell=bash

function main {
      copy __envAirsNewFront__ out \
  &&  aws_login_dev airs \
  &&  sops_export_vars __envAirsSecrets__/development.yaml \
      FONTAWESOME_NPM_AUTH_TOKEN \
  &&  pushd out \
    &&  copy __envAirsNpm__/node_modules 'node_modules' \
    &&  npm install @fortawesome/fontawesome-pro @fortawesome/pro-duotone-svg-icons \
          @fortawesome/pro-light-svg-icons @fortawesome/pro-regular-svg-icons \
          @fortawesome/pro-solid-svg-icons \
    &&  ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    &&  lint_typescript "$(pwd)" "$(pwd)" \
  &&  popd \
  &&  rm -rf out/ \
  ||  return 1
}

main "${@}"
