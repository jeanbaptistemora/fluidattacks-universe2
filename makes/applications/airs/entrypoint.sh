# shellcheck shell=bash

function replace {
  local src="${1}"
  local from="${2}"
  local to="${3}"

  find "${src}" -type f -exec sed -i "s|${from}|${to}|g" {} +
}

function patch_paths {
  local src="${1}"
  local proto="${2}"
  local url="${3}"
  local path="${4}"
  local url_to_replace='please-replace-this-url-before-deploying'
  local path_to_replace='please-replace-this-path-before-deploying'

      replace "${src}" "https://${url_to_replace}" "${proto}://${url}" \
  &&  replace "${src}" "http://${url_to_replace}" "${proto}://${url}" \
  &&  replace "${src}" "${url_to_replace}" "${url}" \
  &&  replace "${src}" "${path_to_replace}" "${path}"
}

function patch_paths_dev {
  patch_paths "${1}" 'http' 'localhost:8000' '/new-front'
}

function patch_paths_eph {
  patch_paths "${1}" 'https' "web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}/new-front" "${CI_COMMIT_REF_NAME}/new-front"
}

function patch_paths_prod {
  patch_paths "${1}" 'https' 'fluidattacks.com/new-front' '/new-front'
}

function main {
  local out="${1}"
  local env="${2:-}"
  local url_to_replace='please-replace-this-url-before-deploying'
  local path_to_replace='please-replace-this-path-before-deploying'

      mkdir -p "${out}" \
  &&  copy __envAirsContent__ "${out}" \
  &&  case "${env}" in
        dev) patch_paths_dev "${out}";;
        eph) patch_paths_eph "${out}";;
        prod) patch_paths_prod "${out}";;
        *)    echo '[ERROR] Second argument must be one of: dev, eph, prod' \
          &&  return 1;;
      esac \
  ||  return 1
}

main "${@}"
