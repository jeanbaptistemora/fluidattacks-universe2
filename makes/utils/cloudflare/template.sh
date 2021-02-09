# shellcheck shell=bash

source '__envUtilsAws__'
source '__envUtilsSops__'

function cloudflare_login {
  local env="${1}"
  local product="${2}"
  local secrets_path="${3}"
  local cloudflare_vars=()

  function get_cloudflare_vars {
    local regex='^CLOUDFLARE[_A-Z]+'

    __envGrep__ -oP "${regex}" "${secrets_path}" | tr '\n' ' '
  }

      "aws_login_${env}" "${product}" \
  &&  IFS=" " read -ra cloudflare_vars <<< "$(get_cloudflare_vars)" \
  &&  echo "${cloudflare_vars[@]}" \
  &&  sops_export_vars "${secrets_path}" \
        "${cloudflare_vars[@]}" \
  &&  for var in "${cloudflare_vars[@]}"
      do
            export "TF_VAR_${var,,}=${!var}" \
        &&  echo "[INFO] Exported: TF_VAR_${var,,}" \
        ||  return 1
      done
}
