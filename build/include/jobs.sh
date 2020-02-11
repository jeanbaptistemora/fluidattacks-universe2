# shellcheck shell=bash

source "${srcIncludeHelpers}"

function job_run_break_build_dynamic {
  helper_run_break_build 'dynamic'
}

function job_run_break_build_static {
  helper_run_break_build 'static'
}

function job_deploy_nix_docker_image {
  local image="${CI_REGISTRY_IMAGE}:test"

    echo "[INFO] Login in: ${CI_REGISTRY}" \
  && docker login \
      --username "${CI_REGISTRY_USER}" \
      --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  && echo "[INFO] Loading: ${dockerImagesLocalNix}" \
  && docker load < "${dockerImagesLocalNix}" \
  && echo "[INFO] Tagging local:test as: ${image}" \
  && docker tag 'local:nix' "${image}" \
  && echo "[INFO] Pushing: ${image}" \
  && docker push "${image}"
}

function job_lint_code {
  local path
  local path_basename

  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2154: var is referenced but not assigned.

      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find '.' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2016,SC2154 {} + \
  && echo '[OK] Shell code is compliant' \
  && hadolint build/Dockerfile \
  && echo '[OK] Dockerfiles are compliant' \
  && find . -type f -name '*.py' \
      | (grep -vP './analytics/singer' || cat) \
      | while read -r path
        do
          echo "[INFO] linting python file: ${path}" \
          && mypy \
                --ignore-missing-imports \
                --no-incremental \
              "${path}" \
          || return 1
        done \
  && pushd analytics/singer \
    && find "${PWD}" -mindepth 1 -maxdepth 1 -type d \
      | while read -r path
        do
          echo "[INFO] linting python package: ${path}" \
          && path_basename=$(basename "${path}") \
          && mypy \
                --ignore-missing-imports \
                --no-incremental \
              "${path_basename}" \
          || return 1
        done \
  && popd \
  && prospector --profile .prospector.yml .
}
