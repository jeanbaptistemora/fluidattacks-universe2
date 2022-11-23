# shellcheck shell=bash

function main {
  for secret in ${envYamlSecrets}; do
    echo "[INFO] Linting ${secret}" \
      && yq -y '[to_entries[] | select(.key != "sops")] | from_entries' "${secret}" > source_file \
      && yamllint --no-warnings --config-file "${envConfig}" 'source_file' \
      || return 1
  done \
    && touch "${out}"
}

main "${@}"
