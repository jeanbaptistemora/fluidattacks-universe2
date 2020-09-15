# shellcheck shell=bash

function _job_common_build_nix_caches {
  local provisioner
  local context='.'
  local dockerfile='build/Dockerfile'

      provisioner=$(basename "${1:-}") \
  &&  provisioner="${provisioner%.*}" \
  &&  helper_docker_build_and_push \
        "${CI_REGISTRY_IMAGE}/nix:${provisioner}" \
        "${context}" \
        "${dockerfile}" \
        'PROVISIONER' "${provisioner}"
}

function job_common_build_nix_caches {
  export TEMP_FILE1
  local provisioners

      helper_use_pristine_workdir \
  &&  provisioners=(./build/provisioners/*) \
  &&  printf "%s\n" "${provisioners[@]}" | LC_ALL=C sort > "${TEMP_FILE1}" \
  &&  helper_execute_chunk_parallel \
        "_job_common_build_nix_caches" \
        "${TEMP_FILE1}"
}

function job_common_send_new_release_email {
      env_prepare_python_packages \
  &&  CI_COMMIT_REF_NAME=master helper_integrates_aws_login 'production' \
  &&  helper_common_sops_env "integrates/secrets-production.yaml" default \
        MANDRILL_APIKEY \
        MANDRILL_EMAIL_TO \
  &&  curl -Lo \
        "${TEMP_FILE1}" \
        'https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/mail.py' \
  &&  echo "send_mail('new_version', MANDRILL_EMAIL_TO,
        context={'project': PROJECT, 'project_url': '$CI_PROJECT_URL',
          'version': _get_version_date(), 'message': _get_message()},
        tags=['general'])" >> "${TEMP_FILE1}" \
  &&  python3 "${TEMP_FILE1}"
}

function job_common_lint_commit_msg {
  local commit_diff
  local commit_hashes

      helper_use_pristine_workdir \
  &&  env_prepare_node_modules \
  &&  git fetch --prune > /dev/null \
  &&  if [ "${IS_LOCAL_BUILD}" = "${TRUE}" ]
      then
            commit_diff="origin/master..${CI_COMMIT_REF_NAME}"
      else
            commit_diff="origin/master..origin/${CI_COMMIT_REF_NAME}"
      fi \
  &&  commit_hashes="$(git log --pretty=%h "${commit_diff}")" \
  &&  for commit_hash in ${commit_hashes}
      do
            git log -1 --pretty=%B "${commit_hash}" | commitlint \
        ||  return 1
      done
}

function job_common_lint_build_system {
  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2153: Possible misspelling: TEMP_FILE2 may not be assigned, but TEMP_FILE1 is.
  # SC2154: var is referenced but not assigned.

      shellcheck --external-sources --exclude=SC2153 build.sh \
  &&  find 'build' 'integrates/mobile/e2e' -name '*.sh' -exec \
        shellcheck --external-sources --exclude=SC1090,SC2016,SC2153,SC2154,SC2064 {} + \
  &&  echo '[OK] Shell code is compliant'
}

function job_common_bugsnag_report {
      export PYTHONPATH=${PYTHONPATH:-}
      env_prepare_python_packages \
  &&  python3 "${STARTDIR}/common/bugsnag-report.py" "${@}"
}

function job_common_test_jobs_provisioner {
  local jobs_output
  local exclude=(
    'forces'
    'skims'
    'skims_pages'
    'integrates_analytics_make_snapshots_prod'
  )

      jobs_output="$(cat build/include/jobs/*)" \
  &&  for file in build/provisioners/*
      do
            provisioner="$(basename "${file%.nix}")" \
        &&  if helper_common_array_contains_element "${provisioner}" "${exclude[@]}"
            then
              echo "[INFO] Provisioner ${provisioner} is excluded. It can exist without a job."
            else
              if { echo "${jobs_output}" | grep -qP "^function job_${provisioner} \{$"; }
              then
                echo "[INFO] Job found for ${provisioner}."
              else
                    echo "[ERROR] Could not find a job for ${provisioner}." \
                &&  return 1
              fi
            fi \
        ||  return 1
      done
}

function job_common_deploy_container_image {
  local context='.'
  local dockerfile='Dockerfile'
  local tag="${CI_REGISTRY_IMAGE}/bin:latest"

      echo '[INFO] Building' \
  &&  helper_use_pristine_workdir \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \

}
