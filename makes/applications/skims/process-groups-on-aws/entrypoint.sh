# shellcheck shell=bash

function main {
  aws_login_prod 'skims' \
    && mapfile -t checks < skims/manifests/findings.lst \
    && mapfile -t checks_dev < skims/manifests/findings.dev.lst \
    && echo "[INFO] Findings to execute: ${checks[*]}" \
    && echo "[INFO] Findings to execute dev: ${checks_dev[*]}" \
    && ensure_gitlab_env_var PRODUCT_API_TOKEN \
    && use_git_repo_services \
    && shopt -s nullglob \
    && for group in "groups/"*; do
      group="$(basename "${group}")" \
        && for check in "${checks[@]}"; do
          MAKES_COMPUTE_ON_AWS_JOB_QUEUE='skims_later' \
            skims-process-group-on-aws "${group}" "${check}" \
            || return 1
        done \
        && for check in "${checks_dev[@]}"; do
          MAKES_COMPUTE_ON_AWS_JOB_QUEUE='skims_dev_later' \
            skims-process-group-on-aws "${group}" "${check}" \
            || return 1
        done \
        || return 1
    done \
    && shopt -u nullglob \
    && popd \
    || return 1
}

main "${@}"
