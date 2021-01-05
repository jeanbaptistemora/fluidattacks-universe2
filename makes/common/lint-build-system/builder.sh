# shellcheck shell=bash

source "${makeDerivation}"

function main {
      find "${envSrcMakes}" -wholename '*.nix' | sort --ignore-case > list \
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
