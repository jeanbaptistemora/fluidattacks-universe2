# shellcheck shell=bash

function format_nix {
  if ! nixpkgs-fmt --check ./*.nix makes > /dev/null
  then
        echo '[ERROR] Source code is not formated with: nixpkgs-fmt' \
    &&  echo '[INFO] We will format it for you, but the job will fail' \
    &&  nixpkgs-fmt ./*.nix makes \
    &&  return 1 \
    ||  return 1
  fi
}

function lint_nix {
  export LANG=C.UTF-8

  # Maybe these two are buggy, worth checking out in the future
  #   AlphabeticalArgs
  #   AlphabeticalBindings

      find makes -wholename '*.nix' | sort --ignore-case > "${LIST}" \
  &&  while read -r path
      do
            echo "[INFO] Testing: ${path}" \
        &&  nix-linter \
              --check=BetaReduction \
              --check=EmptyVariadicParamSet \
              --check=UnneededAntiquote \
              "${path}" \
        ||  return 1
      done < "${LIST}"
}

function lint_shell {
  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC1091: Not following: x: openBinaryFile: does not exist (No such file or directory)
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2153: Possible misspelling: x may not be assigned, but y is.
  # SC2154: x is referenced but not assigned.

      find ./*.sh makes -wholename '*.sh' | sort --ignore-case > "${LIST}" \
  &&  while read -r path
      do
            echo "[INFO] Testing: ${path}" \
        &&  shellcheck \
              --exclude=SC1090,SC1091,SC2016,SC2153,SC2154 \
              --external-sources \
              "${path}" \
        ||  return 1
      done < "${LIST}"
}

function sort_attrs {
  for file in __envMakes__/makes/attrs/*
  do
    if test "$(cat "${file}")" != "$(sort "${file}")"
    then
          echo "[ERROR]: ${file} is not sorted" \
      &&  return 1
    fi
  done
}

function main {
  export LIST

      LIST=$(mktemp) \
  &&  format_nix \
  &&  lint_nix \
  &&  lint_shell \
  &&  sort_attrs \

}

main "${@}"
