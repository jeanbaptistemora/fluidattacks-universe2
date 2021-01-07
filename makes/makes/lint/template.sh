# shellcheck shell=bash

function format_nix {
  if ! __envNixpkgsFmt__ --check makes > /dev/null
  then
        echo '[ERROR] Source code is not formated with: __envNixpkgsFmt__' \
    &&  echo '[INFO] We will format it for you, but the job will fail' \
    &&  __envNixpkgsFmt__ makes \
    &&  return 1 \
    ||  return 1
  fi \
}

function lint_nix {
  export LANG=C.UTF-8

  # Maybe these two are buggy, worth checking out in the future
  #   AlphabeticalArgs
  #   AlphabeticalBindings

      __envFind__ makes -wholename '*.nix' | __envSort__ --ignore-case > "${LIST}" \
  &&  while read -r path
      do
            echo "[INFO] Testing: ${path}" \
        &&  __envNixLinter__ \
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

      __envFind__ makes -wholename '*.sh' | __envSort__ --ignore-case > "${LIST}" \
  &&  while read -r path
      do
            echo "[INFO] Testing: ${path}" \
        &&  __envShellcheck__ \
              --exclude=SC1090,SC1091,SC2016,SC2153,SC2154 \
              --external-sources \
              "${path}" \
        ||  return 1
      done < "${LIST}"
}

function main {
  export LIST

      LIST=$(mktemp) \
  &&  format_nix \
  &&  lint_nix \
  &&  lint_shell \
  &&  success
}

main "${@}"
