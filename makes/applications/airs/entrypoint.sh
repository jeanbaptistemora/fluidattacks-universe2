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
  local src="${1}"

  patch_paths "${src}" 'http' 'localhost:8000' '/new-front'
}

function patch_paths_eph {
  local src="${1}"

  patch_paths "${src}" 'https' "web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}/new-front" "${CI_COMMIT_REF_NAME}/new-front"
}

function patch_paths_prod {
  local src="${1}"

  patch_paths "${src}" 'https' 'fluidattacks.com/new-front' '/new-front'
}

function compress_files {
  local src="${1}"

  find "${src}" -type f -name '*.html' -o -name '*.css' -o -name '*.js' \
    | while read -r file
      do
            gzip -9 "${file}" \
        &&  mv "${file}.gz" "${file}" \
        ||  return 1
      done \
}

function deploy_dev {
  local src="${1}"

      pushd "${src}" \
    &&  python3 -m http.server \
  &&  popd \
  ||  return 1
}

function deploy_eph {
  local src="${1}"

      aws_login_dev airs \
  &&  compress_files "${src}"
}

function deploy_prod {
  local src="${1}"

      aws_login_prod airs \
  &&  compress_files "${src}"
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
        *) abort '[ERROR] Second argument must be one of: dev, eph, prod';;
      esac \
  &&  case "${env}" in
        dev) deploy_dev "${out}";;
        eph) deploy_eph "${out}";;
        prod) deploy_prod "${out}";;
      esac \
  ||  return 1
}

main "${@}"
