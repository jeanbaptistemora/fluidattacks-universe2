#! /usr/bin/env bash

source ./build/include/generic/shell-options.sh

function check_nix_version {
  # Check that Nix is installed
  if ! nix --version
  then
    echo 'Please install nix: https://nixos.org/nix/download.html'
    echo '  on most systems this is:'
    echo '    $ curl https://nixos.org/nix/install | sh'
    return 1
  fi
}

function decide_and_call_provisioner {
  local job="${1:-}"
  local arg1="${2:-}"
  local arg2="${3:-}"
  local arg3="${4:-}"
  local arg4="${5:-}"
  local arg5="${6:-}"
  local arg6="${7:-}"
  local arg7="${8:-}"

  if [[ $job == "common_bugsnag_report" ]]
  then
    shift
    arg1="$*"
  fi
  local provisioner
  local keep=()

  # shellcheck disable=2016
      if echo "${job}" | grep -q 'asserts_test_'
      then
        ./asserts/deploy/dependencies/scripts/odbc/set.sh
      fi \
  &&  provisioner="./build/provisioners/${job}.nix" \
  &&  if [ ! -f "${provisioner}" ]
      then
        provisioner='./build/provisioners/integrates_reset.nix'
      fi \
  &&  echo "[INFO] Running with provisioner: ${provisioner}" \
  &&  while read -r secret
      do keep+=('--keep' "${secret}")
      done < env.lst \
  &&  nix-shell \
        --cores 0 \
        "${keep[@]}" \
        --max-jobs auto \
        --option restrict-eval false \
        --option sandbox false \
        --pure \
        --run '
          source "${srcIncludeGenericShellOptions}"
          source "${srcIncludeCli}"
        '"
          cli ${job} ${arg1} ${arg2} ${arg3} ${arg4} ${arg5} ${arg6} ${arg7}
        " \
        --show-trace \
        "${provisioner}"
}

check_nix_version
if decide_and_call_provisioner "${@}"
then
  decide_and_call_provisioner common_bugsnag_report "passed" "${@}" &>/dev/null || true
else
  decide_and_call_provisioner common_bugsnag_report "failed" "${@}" &>/dev/null
fi
