# shellcheck shell=bash

function main {
  local module="${1:-}"

  if test -n "${module}"
  then
    lint_python_module "__envSrcSkimsSkims__/${module}"
  else
    lint_everything
  fi
}

function lint_everything {
      lint_python_imports '__envImportLinterConfig__' '__envSrcSkimsSkims__' \
  &&  lint_python_module '__envSrcSkimsTest__' \
  &&  lint_python_module '__envSrcProcessGroup__' \
  &&  lint_python_module '__envSrcTestMocksHttp__' \
  &&  for module in "__envSrcSkimsSkims__/"*
      do
            if test -d "${module}"
            then
              lint_python_module "${module}"
            fi \
        ||  return 1
      done
}

main "${@}"
