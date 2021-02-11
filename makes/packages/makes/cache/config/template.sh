# shellcheck shell=bash

function main {
      echo '[INFO] Configuring cache' \
  &&  export MAKES_CACHE_SSH_PRIVATE_KEY="${PWD}/../makes-cache" \
  &&  export MAKES_CACHE_ADDRESS="ssh://ec2-user@192.168.2.33?ssh-key=${MAKES_CACHE_SSH_PRIVATE_KEY}" \
  &&  echo "${MAKES_CACHE_SSH_PRIVATE_KEY_CONTENT}" | __envBase64__ -d > "${MAKES_CACHE_SSH_PRIVATE_KEY}" \
  &&  __envChmod__ 600 "${MAKES_CACHE_SSH_PRIVATE_KEY}" \
  &&  __envSshKeyGen__ -y -f "${MAKES_CACHE_SSH_PRIVATE_KEY}" > "${MAKES_CACHE_SSH_PRIVATE_KEY}.pub"
}

main "${@}"
