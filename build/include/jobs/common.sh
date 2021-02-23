# shellcheck shell=bash

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
    'common_process_on_aws'
    'sorts'
    'observes_code'
    'integrates_analytics_make_snapshots_prod'
    'integrates_reset'
    'integrates_serve_components_legacy'
  )

      jobs_output="$(cat build/include/jobs/* | grep -P '^function job_.+ \{$')" \
  &&  for file in build/provisioners/*
      do
            provisioner="$(basename "${file%.nix}")" \
        &&  if helper_common_array_contains_element "${provisioner}" "${exclude[@]}"
            then
              echo "[INFO] Provisioner ${provisioner} is excluded. It can exist without a job."
            else
              if echo "${jobs_output}" | grep -qP "^function job_${provisioner} \{$"
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
