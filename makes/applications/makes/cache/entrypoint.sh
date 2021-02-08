# shellcheck shell=bash

function main {
  local host='0.0.0.0'
  local port='8888'
  local state_path='.Storage'

      echo __envMinioCli__ \
  &&  __envKillPidListeningOnPort__ "${port}" \
  &&  chmod +x __envMinioCli__ __envMinioLocal__ \
  &&  { MINIO_ACCESS_KEY='test' \
        MINIO_SECRET_KEY='testtest' \
        __envMinioLocal__ server "${state_path}" --address "${host}:${port}" &
      } \
  &&  __envWait__ 10 "${host}:${port}" \
  &&  sleep 1 \
  &&  __envMinioCli__ alias set storage "http://${host}:${port}" 'test' 'testtest' \
  &&  __envMinioCli__ mb --ignore-existing storage/cache \
  &&  __envMinioCli__ policy set public storage/cache  \
  &&  wait
}

main "${@}"
