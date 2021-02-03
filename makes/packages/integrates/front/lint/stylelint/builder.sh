# shellcheck shell=bash

source "${envBashLibCommon}"
source "${envSearchPaths}"

function main {

      copy "${envSrcIntegratesFront}" "${out}" \
  &&  copy "${envSetupIntegratesDevelopmentFront}/node_modules" "${out}/node_modules" \
  &&  copy "${envSetupIntegratesRuntimeFront}/node_modules" "${out}/node_modules" \
  &&  chmod 755 "${out}/node_modules/.bin/stylelint" \
  &&  pushd "${out}" \
    &&  if npm run lint:stylelint
        then
          echo '[INFO] All styles are ok!'
        else
              err_count="$(npx stylelint '**/*.css' | wc -l || true)" \
          &&  echo "[ERROR] ${err_count} errors found in styles!" \
          &&  return 1
        fi \
  &&  popd \
  ||  return 1
}

main "$@"
