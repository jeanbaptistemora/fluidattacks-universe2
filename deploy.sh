#!/usr/bin/env bash

# Compress all HTML, CSS and JS files
while IFS= read -r FILE; do
  gzip -9 "$FILE"
  mv "$FILE.gz" "$FILE";
done < <(find output -type f -name '*.html' -o -name '*.css' -o -name '*.js')

# Upload HTML, CSS and JS files with their respective metadata
EXTENSIONS=(".html" ".css" ".js")
for EXT in "${EXTENSIONS[@]}"; do
  if [ "$EXT" = ".html" ]; then
    CONTENT="text/html";
  fi
  if [ "$EXT" = ".css" ]; then
    CONTENT="text/css";
  fi
  if [ "$EXT" = ".js" ]  ; then
    CONTENT="application/javascript";
  fi
  aws s3 sync --acl public-read --delete --size-only --exclude '*' --include "*$EXT" --metadata-directive REPLACE --content-encoding gzip --content-type "$CONTENT" output/web "s3://$S3_BUCKET_NAME/web";
done

# Upload remaining files
aws s3 sync --acl public-read --delete --size-only output/web "s3://$S3_BUCKET_NAME/web"
