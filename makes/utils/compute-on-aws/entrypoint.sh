# shellcheck shell=bash

source '__envUtilsBashLibAws__'

function substitute_env_vars {
  '__envEnvsubst__' -no-empty -no-unset < "${1}"
}

function in_queue {
  local job_name="${1}"
  local queue="${2}"
  local status="${3}"

      in_queue=$( \
        '__envAws__' batch list-jobs \
          --job-queue "${queue}" \
          --job-status "${status}" \
          --query 'jobSummaryList[*].jobName' \
          | '__envJq__' -r \
              --arg 'job_name' "${job_name}" \
              '. | contains([$job_name])' \
      ) \
  &&  echo "${in_queue}"
}

function is_already_in_queue {
  local job_name="${1}"
  local queue="${2}"
  local found=0
  local check_status

      check_status=(
        "SUBMITTED"
        "PENDING"
        "RUNNABLE"
        "STARTING"
        "RUNNING"
      ) \
  &&  for status in "${check_status[@]}"
      do
        if test "$(in_queue "${job_name}" "${queue}" "${status}")" = 'true'
        then
          found=1
          break
        fi
      done
      if test "${found}" = "1"
      then
        echo 'true'
      else
        echo 'false'
      fi
}

function main {
  local env_command
  local env_jobname
  local env_manifest

      env_command="$(substitute_env_vars '__envCommandFile__')" \
  &&  env_jobname='__envJobname__' \
  &&  for arg in "${@:1}"
      do
        env_jobname="${env_jobname}-${arg}"
      done \
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
  &&  if test "$(is_already_in_queue "${env_jobname}" '__envJobqueue__')" = 'false'
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
