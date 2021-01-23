# shellcheck shell=bash

# Shell hardening
set -o errexit
set -o pipefail
set -o nounset
set -o functrace
set -o errtrace
set -o monitor
set -o posix

# https://reproducible-builds.org/docs/source-date-epoch/
# https://nixos.org/nixpkgs/manual/#faq (15.17.3.3)
unset SOURCE_DATE_EPOCH
