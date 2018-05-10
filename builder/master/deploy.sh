#!/usr/bin/env bash

# This script compresses the HTML, CSS and JS files in order to improve
# page loading speed. It also sets their respective metadata during upload
# so they are identified correctly and the website displays as intended.

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
            CONTENT="--content-type text/html"
            ENCODING="--content-encoding gzip"
            ;;
    ".css")
            CONTENT="--content-type text/css"
            ENCODING="--content-encoding gzip"
            ;;
    ".js")
            CONTENT="--content-type application/javascript"
            ENCODING="--content-encoding gzip"
            ;;
    ".png")
            CONTENT="--content-type image/png"
            ENCODING=""
            ;;
  esac
  aws s3 sync --acl public-read --delete --size-only --exclude '*' \
    --include "*$EXT" --metadata-directive REPLACE "$ENCODING" \
    "$CONTENT" output/web "s3://$S3_BUCKET_NAME/web";
done

# Upload remaining files
aws s3 sync --acl public-read --delete --size-only \
  output/web "s3://$S3_BUCKET_NAME/web"
