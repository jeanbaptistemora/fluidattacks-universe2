# shellcheck disable=SC2043 shell=bash

function main {
  # Try to export okta and cloudflare vars if secrets provided
  aws_login_prod '__envProduct__' \
    && if test -n '__envSecretsPath__'; then
      sops_export_vars_terraform \
        '__envSecretsPath__' \
        'CLOUDFLARE'
    fi \
    && for var in __envVars__; do
      ensure_env_var "${var}" \
        && export "TF_VAR_${var}=${!var}"
    done \
    && pushd '__envTarget__' \
    && echo '[INFO] Initializing' \
    && terraform init \
    && echo '[INFO] Refreshing state' \
    && terraform refresh \
    && for resource in "${@}"; do
      echo "[INFO] Tainting ${resource}" \
        && terraform taint "${resource}" \
        || return 1
    done \
    && popd \
    || return 1
}

main "${@}"
