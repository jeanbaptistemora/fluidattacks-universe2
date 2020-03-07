#!/usr/bin/env bash

aws_login() {
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    AWS_ACCESS_KEY_ID="$PROD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY="$PROD_AWS_SECRET_ACCESS_KEY"
  else
    AWS_ACCESS_KEY_ID="$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY="$DEV_AWS_SECRET_ACCESS_KEY"
  fi
}

terraform_login() {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  aws_login

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
}

function sync_s3 {
  # Synchronize <source_code> in <bucket>

  local source_code="${1}"
  local bucket_path="${2}"
  local extensions=('html' 'css' 'js' 'png' 'svg')

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
