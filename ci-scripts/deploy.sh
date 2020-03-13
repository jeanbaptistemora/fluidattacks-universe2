#!/usr/bin/env bash

# shellcheck disable=SC1091

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
      "${source_code}/"                \
      "s3://${bucket_path}/"           \
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
  if mv "${CI_PROJECT_DIR}/cache" /app/cache; then
    echo '[INFO] Moving cache to /app folder.'
  else
    echo '[INFO] No cache found.'
  fi
  cp -a /app/deploy/builder/node_modules /app/theme/2014/
  cp -a /app/deploy/builder/node_modules /app/
  npm run --prefix /app/deploy/builder/ build
  /app/build-site.sh
  sync_s3 /app/output/ web.fluidattacks.com
  mv /app/cache "${CI_PROJECT_DIR}/cache"
  popd || return 1
}

function deploy_prod_new {
  pushd /app/new || return 1
  if mv "${CI_PROJECT_DIR}/new/cache" /app/new/cache; then
    echo '[INFO] Moving cache of the new site to app/new folder.'
  else
    echo '[INFO] No cache found.'
  fi
  cp -a /app/deploy/builder/node_modules /app/new/theme/2020/
  cp -a /app/deploy/builder/node_modules /app/new
  npm run --prefix /app/deploy/builder/ build-new
  /app/new/build-site.sh
  cp -a /app/new/output/newweb /app/output
  popd || return 1
  sync_s3 /app/output/ web.fluidattacks.com
  mv /app/new/cache "${CI_PROJECT_DIR}/new/cache"
}

function deploy_eph {
  pushd /app || return 1
  if mv "${CI_PROJECT_DIR}/cache" /app/cache; then
    echo '[INFO] Moving cache to /app folder.'
  else
    echo '[INFO] No cache found.'
  fi
  cp -a /app/deploy/builder/node_modules /app/theme/2014/
  cp -a /app/deploy/builder/node_modules /app/
  sed -i "s|https://fluidattacks.com|https://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}|g" /app/pelicanconf.py
  npm run --prefix /app/deploy/builder/ build
  /app/build-site.sh
  /app/html-lint.sh
  sync_s3 /app/output/ "web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}"
  mv /app/cache "${CI_PROJECT_DIR}/cache"
  popd || return 1
}
