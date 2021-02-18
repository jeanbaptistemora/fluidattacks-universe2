#! __envShell__
# shellcheck shell=bash

source __envBashLibShopts__

function setup {
  export GEM_PATH='/no-gem-path'
  export HOME
  export HOME_IMPURE
  export LD_LIBRARY_PATH='/no-ld-library-path'
  export NODE_PATH='/no-node-path'
  export PATH='/no-path'
  export PYTHONPATH='/no-pythonpath'
  export SSL_CERT_FILE='__envCaCert__/etc/ssl/certs/ca-bundle.crt'

      source __envSearchPathsBase__ \
  &&  if test -z "${HOME_IMPURE:-}"
      then
            HOME_IMPURE="${HOME}" \
        &&  HOME="$(mktemp -d)"
      fi \
  &&  source __envBashLibCommon__ \
  &&  source __envSearchPaths__
}

setup
