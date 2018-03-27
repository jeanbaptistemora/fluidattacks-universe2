#!/usr/bin/env bash

PATTERN="output/"
PATTERN2="/index.html"

find output -iname '*.html' | while IFS= read -r FILE; do
  STRING=${FILE/$PATTERN/}
  NAME=${STRING/$PATTERN2/}
  if [[ ! $NAME = *".html" ]]; then
    aws s3api put-object --acl public-read \
    --bucket "$S3_BUCKET_NAME" --key "$NAME" --content-type text/html \
    --website-redirect-location "/$NAME/";
  fi;
done
