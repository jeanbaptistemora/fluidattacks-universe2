# shellcheck shell=bash

function lint_nix {
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
      done < list
}

function lint_shell {
  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC1091: Not following: x: openBinaryFile: does not exist (No such file or directory)
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2153: Possible misspelling: x may not be assigned, but y is.
  # SC2154: x is referenced but not assigned.

      copy "${envSrcMakes}" "${PWD}/makes" \
  &&  find . -wholename '*.sh' | sort --ignore-case > list \
  &&  while read -r path
      do
            echo "[INFO] Testing: ${path}" \
        &&  shellcheck \
              --exclude=SC1090,SC1091,SC2016,SC2153,SC2154 \
              --external-sources \
              "${path}" \
        ||  return 1
      done < list
}

function main {
      lint_nix \
  &&  lint_shell \
  &&  success
}

main "${@}"
