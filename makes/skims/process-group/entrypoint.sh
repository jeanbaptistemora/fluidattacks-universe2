# shellcheck shell=bash

source '__envSetupSkimsRuntime__'
source '__envUtilsBashLibAws__'
source '__envUtilsBashLibSops__'

function main {
  local group="${1:-}"
  local cache_local="${HOME}/.skims"
  local cache_remote="s3://skims.data/cache/${group}"

      if test -z "${group}"
      then
            echo '[ERROR] Specify the group on the first argument to this program' \
        &&  return 1
      fi \
  &&  echo "[INFO] Processing ${group}" \
  &&  aws_login_prod 'skims' \
  &&  aws_s3_sync "${cache_remote}" "${cache_local}" \
  &&  __envSkims__ --help \
  &&  echo '[INFO] Populating cache' \
  &&  aws_s3_sync "${cache_local}" "${cache_remote}" \
  ||  return 1
}

main "${@}"
