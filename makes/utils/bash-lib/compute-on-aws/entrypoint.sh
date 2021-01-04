# shellcheck shell=bash

source '__envUtilsBashLibAws__'

function substitute_env_vars {
  cat "${1}" | '__envEnvsubst__' -no-empty -no-unset
}

function main {
  local env_command
  local env_jobname
  local env_manifest

      env_command="$(substitute_env_vars '__envCommandFile__')" \
  &&  env_jobname='__envJobname__' \
  &&  if test -n "${*:1}"
      then
        env_jobname="${env_jobname}-${*:1}"
      fi \
  &&  env_manifest="$(substitute_env_vars '__envManifestFile__')" \
  &&  env_command="$( \
        __envJq__ \
          -enr \
          --argjson 'command' "${env_command}" \
          --args \
          '($command + $ARGS.positional)' \
          -- \
          "${@}" \
      )" \
  &&  echo "[INFO] Running on AWS: ${env_command}" \
  &&  echo '[INFO] VCPUs: __envVcpus__' \
  &&  echo '[INFO] Memory: __envMemory__ MB' \
  &&  echo '[INFO] Attempts: __envAttempts__' \
  &&  echo '[INFO] Timeout: __envTimeout__ seconds' \
  &&  echo "[INFO] Job Name: ${env_jobname}" \
  &&  echo '[INFO] Job Queue: __envJobqueue__' \
  &&  aws_login_prod '__envProduct__' \
  &&  is_already_in_queue=$( \
        '__envAws__' batch list-jobs \
          --job-queue '__envJobqueue__' \
          --job-status 'RUNNABLE' \
          --query 'jobSummaryList[*].jobName' \
          | '__envJq__' -r \
              --arg 'env_jobname' "${env_jobname}" \
              '. | contains([$env_jobname])' \
      ) \
  &&  if test "${is_already_in_queue}" = 'false'
      then
            echo '[INFO] Sending job' \
        &&  '__envAws__' batch submit-job \
              --container-overrides "$( \
                __envJq__ \
                  -enr \
                  --argjson 'manifest' "${env_manifest}" \
                  --argjson 'command' "${env_command}" \
                  --args \
                  '$manifest * {command: $command}'
              )" \
              --job-name "${env_jobname}" \
              --job-queue '__envJobqueue__' \
              --job-definition 'default' \
              --retry-strategy 'attempts=__envAttempts__' \
              --timeout 'attemptDurationSeconds=__envTimeout__' \
        &&  echo "[INFO] Job ${env_jobname} has been succesfully sent"
      else
        echo "[INFO] Job ${env_jobname} is already in queue, skipped sending it"
      fi
}

main "${@}"
