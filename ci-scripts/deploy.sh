#!/usr/bin/env bash

# shellcheck disable=SC1091

function get_cache {
  # Get cache artifact from last successful branch pipeline

  local job="${1}"
  local token="${2}"
  local base_url="https://gitlab.com/api/v4/projects/4649627"
  local job_url="${base_url}/jobs/artifacts/${CI_COMMIT_REF_NAME}/download?job=${job}"
  local token_header="PRIVATE-TOKEN: ${token}"

  if curl -H "${token_header}" -fLo artifacts.zip "${job_url}"; then
      unzip artifacts.zip
      rm -rf artifacts.zip
    else
      echo "[INFO] There are no artifacts."
  fi
}

function sync_s3 {
  # Synchronize <source_code> in <bucket>

  local source_code="${1}"
  local bucket_path="${2}"
  local extensions=('html' 'css' 'js' 'png' 'svg')

  source ci-scripts/helpers/others.sh

  aws_login

  # Compress all HTML, CSS and JS files and remove the .gz extension
  while IFS= read -r file; do
    gzip -9 "${file}"
    mv "${file}.gz" "${file}";
  done < <(find "${source_code}" -type f -name '*.html' -o -name '*.css' -o -name '*.js')

  # Set correct metadata according to the compressed file and upload them
  for extension in "${extensions[@]}"; do
    local compress
    local content_type
    case ${extension} in
      'html')
        content_type='text/html'
        compress='gzip'
        ;;
      'css')
        content_type='text/css'
        compress='gzip'
        ;;
      'js')
        content_type='application/javascript'
        compress='gzip'
        ;;
      'png')
        content_type='image/png'
        compress='identity'
        ;;
      'svg')
        content_type='image/svg+xml'
        compress='identity'
        ;;
      *)
        content_type='application/octet-stream'
        compress='identity'
        ;;
    esac
    aws s3 sync                        \
      "${source_code}/web"             \
      "s3://${bucket_path}/web"        \
      --acl public-read                \
      --exclude "*"                    \
      --include "*.${extension}"       \
      --metadata-directive REPLACE     \
      --content-type "${content_type}" \
      --content-encoding "${compress}" \
      --delete
  done

  # Upload remaining files
  aws s3 sync            \
  "${source_code}/"      \
  "s3://${bucket_path}/" \
  --exclude "*.html"     \
  --exclude "*.css"      \
  --exclude "*.js"       \
  --exclude "*.png"      \
  --exclude "*.svg"      \
  --delete
}

function deploy_prod {
  pushd /app || return 1
  get_cache production "${GITLAB_API_TOKEN}"
  cp -a /app/deploy/builder/node_modules /app/theme/2014/
  cp -a /app/deploy/builder/node_modules /app/
  npm run --prefix /app/deploy/builder/ build
  /app/build-site.sh
  sync_s3 /app/output/ web.fluidattacks.com
  mv /app/cache "${CI_PROJECT_DIR}/cache"
  popd || return 1
}

function deploy_eph {
  pushd /app || return 1
  get_cache ephemeral "${GITLAB_API_TOKEN}"
  cp -a /app/deploy/builder/node_modules /app/theme/2014/
  cp -a /app/deploy/builder/node_modules /app/
  sed -i "s|https://fluidattacks.com|http://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}|g" /app/pelicanconf.py
  npm run --prefix /app/deploy/builder/ build
  /app/build-site.sh
  cp -a /app/deploy/ephemeral/index.html /app/output/
  cp -a /app/deploy/ephemeral/index-error.html /app/output/
  /app/html-lint.sh
  sync_s3 /app/output/ "web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}"
  mv /app/cache "${CI_PROJECT_DIR}/cache"
  popd || return 1
}
