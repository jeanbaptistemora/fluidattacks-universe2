#!/usr/bin/env bash

# This script compresses the HTML, CSS and JS files in order to improve
# page loading speed. It also sets their respective metadata during upload
# so they are identified correctly and the website displays as intended.

source ci-scripts/helpers/others.sh
aws_login

# Compress all HTML, CSS and JS files and remove the .gz extension
while IFS= read -r FILE; do
  gzip -9 "$FILE"
  mv "$FILE.gz" "$FILE";
done < <(find output -type f -name '*.html' -o -name '*.css' -o -name '*.js')

# Set correct metadata according to the compressed file and upload them
EXTENSIONS=(".html" ".css" ".js" ".png")
for EXT in "${EXTENSIONS[@]}"; do
  case $EXT in
    ".html")
            aws s3 sync output/web "s3://$S3_BUCKET_NAME/web" --acl public-read --exclude "*" --include "*.html" --metadata-directive REPLACE --content-type text/html --content-encoding gzip --delete
            ;;
    ".css")
            aws s3 sync output/web "s3://$S3_BUCKET_NAME/web" --acl public-read --exclude "*" --include "*.css" --metadata-directive REPLACE --content-type text/css --content-encoding gzip --delete
            ;;
    ".js")
            aws s3 sync output/web "s3://$S3_BUCKET_NAME/web" --acl public-read --exclude "*" --include "*.js" --metadata-directive REPLACE --content-type application/javascript --content-encoding gzip --delete
            ;;
    ".png")
            aws s3 sync output/web "s3://$S3_BUCKET_NAME/web" --acl public-read --exclude "*" --include "*.png" --metadata-directive REPLACE --content-type image/png --delete
            ;;
  esac
done

# Upload remaining files
aws s3 sync output/ "s3://$S3_BUCKET_NAME/" --exclude "*.html" --exclude "*.css" --exclude "*.js" --exclude "*.png" --delete
