# shellcheck shell=bash

function main {
  local nix_store_path="${1}"
  export PATH="__envSsh__/bin:${PATH}"

      echo "[INFO] Signing paths: ${nix_store_path}" \
  &&  key_file=$(mktemp) \
  &&  echo "${MAKES_CACHE_PRIVATE_KEY}" > "${key_file}" \
  &&  __envNix__ sign-paths --key-file "${key_file}" --recursive "${nix_store_path}" \
  &&  echo "[INFO] Pushing to cache: ${nix_store_path}" \
  &&  __envNix__ copy --to "${MAKES_CACHE_ADDRESS}" "${nix_store_path}" \
  &&  echo "[INFO] Pushed: ${nix_store_path}"
}

main "${@}"
