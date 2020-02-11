# shellcheck shell=bash

function job_all {
  local function_to_call

  # Execute all job functions except this mere one
  helper_list_declared_jobs | while read -r function_to_call
  do
    echo "[INFO] Executing function: ${function_to_call}"
    test "${function_to_call}" = "job_all" \
      || "${function_to_call}" \
      || return 1
  done
}

function job_deploy_nix_docker_image {
  local image="${CI_REGISTRY_IMAGE}:nix"

    echo "[INFO] Login in: ${CI_REGISTRY}" \
  && docker login \
      --username "${CI_REGISTRY_USER}" \
      --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  && echo "[INFO] Pulling: ${image}" \
  && docker pull "${image}" || true \
  && echo "[INFO] Building: ${image}" \
  && docker build --tag "${image}" --file './build/Dockerfile' '.' \
  && echo "[INFO] Pushing: ${image}" \
  && docker push "${image}"
}

function job_lint_build_code {
      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find 'build' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2154, {} + \
  && echo '[OK] Shell code is compliant' \
  && hadolint build/Dockerfile \
  && echo '[OK] Dockerfiles are compliant'
}

function job_lint_touched_code {
  prospector --profile .prospector.yml .

  helper_list_touched_files_in_last_commit \
    | xargs pre-commit run --verbose --files
}
