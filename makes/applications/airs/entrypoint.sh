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

  patch_paths "${src}" 'http' 'localhost:8000' 'new-front'
}

function patch_paths_eph {
  local src="${1}"

  patch_paths "${src}" 'https' "web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}/new-front" "${CI_COMMIT_REF_NAME}/new-front"
}

function patch_paths_prod {
  local src="${1}"

  patch_paths "${src}" 'https' 'fluidattacks.com/new-front' 'new-front'
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

function sync_files {
  local src="${1}"
  local target="${2}"
  declare -A content_encodings=(
    [css]=gzip
    [html]=gzip
    [js]=gzip
    [png]=identity
    [svg]=identity
  )
  declare -A content_types=(
    [css]=text/css
    [html]=text/html
    [js]=application/javascript
    [png]=image/png
    [svg]=image/svg+xml
  )

      for ext in "${!content_encodings[@]}"
      do
            content_encoding="${content_encodings[${ext}]}" \
        &&  content_type="${content_types[${ext}]}" \
        &&  aws s3 sync \
              "${src}" \
              "${target}" \
              --acl private \
              --delete \
              --content-encoding "${content_encoding}" \
              --content-type "${content_type}" \
              --exclude '*' \
              --include "*.${ext}" \
              --metadata-directive REPLACE \
        ||  return 1
      done \
  &&  aws s3 sync \
        "${src}" \
        "${target}" \
        --delete \
        --exclude '*.css' \
        --exclude '*.html' \
        --exclude '*.js' \
        --exclude '*.png' \
        --exclude '*.svg'
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
  &&  compress_files "${src}" \
  &&  sync_files "${src}" "s3://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}" \
  &&  announce_to_bugsnag ephemeral
}

function deploy_prod {
  local src="${1}"

      aws_login_prod airs \
  &&  compress_files "${src}" \
  &&  sync_files "${src}" 's3://fluidattacks.com' \
  &&  announce_to_bugsnag production
}

function stop_eph {
      aws_login_dev airs \
  &&  aws s3 rm --recursive "s3://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}"
}

function announce_to_bugsnag {
  local release_stage="${1}"

  makes-announce-bugsnag 6d0d7e66955855de59cfff659e6edf31 "${release_stage}"
}

function main {
  local env="${1:-}"
  local out='airs/output'
  local url_to_replace='please-replace-this-url-before-deploying'
  local path_to_replace='please-replace-this-path-before-deploying'

      __envAirsContent__ "${out}" \
  &&  case "${env}" in
        dev) patch_paths_dev "${out}";;
        eph) patch_paths_eph "${out}";;
        eph-stop) :;;
        prod) patch_paths_prod "${out}";;
        *) abort '[ERROR] Second argument must be one of: dev, eph, prod';;
      esac \
  &&  case "${env}" in
        dev) deploy_dev "${out}";;
        eph) deploy_eph "${out}";;
        eph-stop) stop_eph;;
        prod) deploy_prod "${out}";;
      esac \
  ||  return 1
}

main "${@}"
