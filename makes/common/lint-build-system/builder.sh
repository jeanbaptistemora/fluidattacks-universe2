# shellcheck shell=bash

source "${makeDerivation}"

function main {
  export LANG=C.UTF-8

  # Maybe these two are buggy, worth checking out in the future
  #   AlphabeticalArgs
  #   AlphabeticalBindings

      copy "${envSrcMakes}" "${PWD}/makes" \
  &&  find . -wholename '*.nix' | sort --ignore-case > list \
  &&  while read -r path
      do
            echo "[INFO] Testing: ${path}" \
        &&  nix-linter \
              --check=BetaReduction \
              --check=EmptyVariadicParamSet \
              --check=UnneededAntiquote \
              "${path}" \
        ||  return 1
      done < list \
  &&  success
}

main "${@}"
