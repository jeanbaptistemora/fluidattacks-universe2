# shellcheck shell=bash

function main {
      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesFrontDevRuntime}/node_modules" "${out}/node_modules" \
  &&  pushd "${out}" \
    &&  ./node_modules/.bin/tcm src/ --silent \
    &&  ./node_modules/.bin/tsc -p tsconfig.json \
    &&  ./node_modules/.bin/eslint . --ext .js,.ts,.tsx --format codeframe \
  &&  popd \
  && echo_env_config \
  ||  return 1
}

main "$@"
