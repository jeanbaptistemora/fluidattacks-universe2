# shellcheck shell=bash

source '__envUtilsBashLibPython__'

function forces_setup_wrapper {
      make_python_path '3.8' \
        '__envPythonRequirements__'
}

function forces {
  export SSL_CERT_FILE='__envCacert__/etc/ssl/certs/ca-bundle.crt'

  '__envPython__' '__envForces__' "$@"
}

forces_setup_wrapper
